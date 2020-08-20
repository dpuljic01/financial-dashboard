import json
from flask_jwt_extended import jwt_required, get_jwt_identity

import pymongo
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from server.models import Stock
from server.apis.iex import IEXFinance
from server.apis.yfinance import fetch_stock_history, fetch_stock_info
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


@bp.route("/yfinance/<string:symbol>", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=300, key_prefix=make_cache_key)
def yf_stock_quote(symbol):
    quote = fetch_stock_info(symbol)
    return jsonify(quote)


@bp.route("/yfinance", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=300, key_prefix=make_cache_key)
@use_args({
    "period": fields.Str(missing="1d"),
    "interval": fields.Str(missing="30m"),
    "symbols": fields.DelimitedList(fields.Str(), required=True),
    "start": fields.Str(missing=None),
    "end": fields.Str(missing=None),
}, location="query")
def yfinance_quote_history(args):
    current_identity = get_jwt_identity()
    history = fetch_stock_history(
        tickers=args["symbols"],
        period=args["period"],
        interval=args["interval"],
        start=args["start"],
        end=args["end"],
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
@use_args({
    "q": fields.Str(required=True),
}, location="query")
def search_iex_companies(args):
    symbol = IEXFinance.search(args["q"])
    return jsonify(symbol)


# this search queries mongo_db
@bp.route("/search", methods=["GET"])
@use_args({
    "q": fields.Str(required=True),
}, location="query")
def aggregate_search_mongodb(args):
    tickers_collection = pymongo.collection.Collection(mongo_db, "tickers")
    symbols = tickers_collection.aggregate([{
        "$match":
            {
                "$or": [
                    {"symbol": {"$regex": f"^{args['q']}", "$options": "$i"}},
                    {"name": {"$regex": f"^{args['q']}", "$options": "$i"}},
                ]
            },
        },
        {"$limit": 5}
    ])
    return jsonify(json.loads(dumps(symbols)))


@bp.route("/alpha-timeseries", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=30, key_prefix=make_cache_key)
@use_args({
    "function": fields.Str(required=True),
    "interval": fields.Str(),
    "symbol": fields.Str(required=True),
    "start": fields.Str(missing=None),
    "end": fields.Str(missing=None),
}, location="query")
def alpha_vantage_info(args):
    current_identity = get_jwt_identity()
    resp = AlphaVantage.fetch_data(args)
    return jsonify(resp)