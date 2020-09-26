import json
from flask_jwt_extended import jwt_required

import pymongo
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args

from server.common.common import slugify_keys, to_local_datetime
from server.models import Stock
from server.apis.iex import IEXFinance
from server.apis.nasdaq import Nasdaq
from server.apis.yfinance import (
    fetch_stock_history,
    fetch_stock_info,
    get_quote,
    get_stock_recommendations,
)
from server.apis.alpha_vantage import AlphaVantage
from server.decorators import check_confirmed
from server.extensions import cache, db
from server.mongo_db import mongo_db

bp = Blueprint("tickers", __name__, url_prefix="/api/stocks")


def make_cache_key(*args, **kwargs):
    return request.url


@bp.route("/<string:symbol>", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=300, key_prefix=make_cache_key)
def get_stock(symbol):
    symbol = symbol.upper()
    stock_db = Stock.query.filter_by(ticker=symbol).first_or_404()

    params = {"function": "GLOBAL_QUOTE", "symbol": symbol}
    global_quote = AlphaVantage.fetch_data(params)
    stock_db.info = AlphaVantage.filter_global_quote(global_quote)
    db.session.commit()
    return jsonify(stock_db.json)


@bp.route("/iex/<string:symbol>", methods=["GET"])
@jwt_required
@check_confirmed
def iex_stock_quote(symbol):
    quote = IEXFinance.get_stock_quote(symbol)
    return jsonify(quote)


@bp.route("/nasdaq/<string:symbol>/info", methods=["GET"])
@jwt_required
@check_confirmed
def nasdaq_stock_info(symbol):
    quote = Nasdaq.stock_info(symbol)
    return jsonify(quote)


@bp.route("/nasdaq/market-movers", methods=["GET"])
@jwt_required
@check_confirmed
def nasdaq_market_movers():
    movers = Nasdaq.get_market_movers()
    return jsonify(slugify_keys(movers["data"]["STOCKS"]))


@bp.route("/<string:symbol>/recommendations", methods=["GET"])
@jwt_required
@check_confirmed
def recommendations(symbol):
    r = get_stock_recommendations(symbol)
    r = [{to_local_datetime(int(k) / 1000): slugify_keys(v)} for k, v in r.items()]
    return jsonify(r)


@bp.route("/yfinance/<string:symbol>", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=10, key_prefix=make_cache_key)
def yf_stock_quote(symbol):
    quote = get_stock_recommendations(symbol)
    return jsonify(quote)


@bp.route("/<string:symbol>/company-info", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=60 * 5, key_prefix=make_cache_key)
def get_company_info(symbol):
    symbol = symbol.upper()
    stock = Stock.query.filter_by(ticker=symbol).one_or_none()

    # for faster loading, fetch already existing info from DB TODO: see when to update DB with fresh info
    if stock:
        if not stock.company_info:
            stock.company_info = slugify_keys(
                fetch_stock_info(symbol)
            )  # company profile
        return jsonify(stock.company_info)

    # recommendations = IEXFinance.get_recommendations(symbol)
    # company_info.update({"recommendations": recommendations})
    company_info = slugify_keys(fetch_stock_info(symbol))
    stock_db = Stock(
        ticker=symbol,
        short_name=company_info["shortname"],
        company_info=company_info,
    )
    db.session.add(stock_db)
    db.session.commit()
    return jsonify(company_info)


@bp.route("/yfinance", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=60 * 5, key_prefix=make_cache_key)
@use_args(
    {
        "period": fields.Str(missing="2d"),
        "interval": fields.Str(missing="15m"),
        "symbols": fields.DelimitedList(fields.Str(), required=True),
        "start": fields.Str(missing=None),
        "end": fields.Str(missing=None),
        "include_info": fields.Bool(missing=False),
    },
    location="query",
)
def yfinance_quote_history(args):
    history = fetch_stock_history(
        tickers=args["symbols"],
        period=args["period"],
        interval=args["interval"],
        start=args["start"],
        end=args["end"],
        include_info=args["include_info"],
    )
    return jsonify(history)


@bp.route("/iex/symbols", methods=["GET"])
@jwt_required
@check_confirmed
def list_iex_cloud_symbols():
    symbols = IEXFinance.list_symbols()
    return jsonify(symbols)


# this search calls iex api
@bp.route("/iex/symbols/search", methods=["GET"])
@use_args(
    {
        "q": fields.Str(required=True),
    },
    location="query",
)
def search_iex_companies(args):
    symbol = IEXFinance.search(args["q"])
    return jsonify(symbol)


# this search queries mongo_db
@bp.route("/search", methods=["GET"])
@use_args(
    {
        "q": fields.Str(required=True),
    },
    location="query",
)
def aggregate_search_mongodb(args):
    tickers_collection = pymongo.collection.Collection(mongo_db, "tickers")
    symbols = tickers_collection.aggregate(
        [
            {
                "$match": {
                    "$or": [
                        {"symbol": {"$regex": f"^{args['q']}", "$options": "$i"}},
                        {"name": {"$regex": f"^{args['q']}", "$options": "$i"}},
                    ]
                },
            },
            {"$limit": 5},
        ]
    )
    return jsonify(json.loads(dumps(symbols)))


@bp.route("/alpha-timeseries", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=30, key_prefix=make_cache_key)
@use_args(
    {
        "function": fields.Str(required=True),
        "interval": fields.Str(),
        "symbol": fields.Str(required=True),
        "start": fields.Str(missing=None),
        "end": fields.Str(missing=None),
    },
    location="query",
)
def alpha_vantage_info(args):
    resp = AlphaVantage.fetch_data(args)
    return jsonify(resp)


@bp.route("/yfinance/latest", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=60, key_prefix=make_cache_key)
@use_args(
    {
        "symbols": fields.DelimitedList(fields.Str(), required=True),
    },
    location="query",
)
def fetch_latest_stock_prices(args):
    args["symbols"] = [symbol.upper() for symbol in args["symbols"]]
    stocks = Stock.query.filter(Stock.ticker.in_(args["symbols"])).all()
    if not stocks:
        return jsonify({"message": "Symbols not found in database"}), 404

    res = []
    for stock in stocks:
        quote = {}
        try:
            quote = get_quote(stock.ticker)[stock.ticker]
        except:
            pass

        if quote:
            res.append(quote)
            stock.latest_market_data = slugify_keys(quote)
            db.session.commit()
            continue

        params = {"function": "GLOBAL_QUOTE", "symbol": stock.ticker}
        global_quote = AlphaVantage.fetch_data(params)
        if global_quote.get("Global Quote", {}):
            quote = AlphaVantage.filter_global_quote(global_quote)
            res.append(quote)
            stock.latest_market_data = slugify_keys(quote)
            db.session.commit()
            continue

        quote = IEXFinance.get_stock_quote(ticker=stock.ticker)
        if not quote:
            print("IEXFinance quote fetch failed")
            continue

        if quote["changePercent"]:
            quote["changePercent"] = quote["changePercent"] * 100
        res.append(quote)
        stock.latest_market_data = slugify_keys(quote)
        db.session.commit()
    db.session.commit()

    return jsonify(res), 204
