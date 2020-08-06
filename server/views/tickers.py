from flask import Blueprint, jsonify
from server.apis.iex import IEXFinance
from server.apis.yfinance import fetch_stock_history
from webargs.flaskparser import use_args
from webargs import fields

bp = Blueprint("tickers", __name__, url_prefix="/api/stocks")


@bp.route("/iex/<string:symbol>", methods=["GET"])
def iex_stock_quote(symbol):
    quote = IEXFinance.get_stock_quote(symbol)
    return jsonify(quote)


@bp.route("/yfinance", methods=["GET"])
@use_args({
    "period": fields.Str(missing="1d"),
    "interval": fields.Str(missing="30m"),
    "symbols": fields.DelimitedList(fields.Str(), required=True),
    "start": fields.Str(missing=None),
    "end": fields.Str(missing=None),
}, location="query")
def yfinance_stock_quote(args):
    history = fetch_stock_history(
        tickers=args["symbols"],
        period=args["period"],
        interval=args["interval"],
        start=args["start"],
        end=args["end"],
    )
    return jsonify(history)


@bp.route("/symbols", methods=["GET"])
def list_iex_cloud_symbols():
    symbols = IEXFinance.list_symbols()
    return jsonify(symbols)


@bp.route("/symbols/search", methods=["GET"])
@use_args({
    "symbol": fields.Str(required=True),
}, location="query")
def search_symbol(args):
    symbol = IEXFinance.search_symbol(args["symbol"])
    return jsonify(symbol)
