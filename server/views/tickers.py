from flask import Blueprint, request, jsonify
from server.models import Stock
from server.apis.iex import IEXFinance


bp = Blueprint("tickers", __name__, url_prefix="/api/stocks")


@bp.route("/<string:symbol>", methods=["GET"])
def stock_quote(symbol):
    quote = IEXFinance.get_stock_quote(symbol)
    return jsonify(quote)


# @bp.route("/autocomplete", methods=["GET"])
# def autocomplete():
#     term = request.args.get("q").upper()
#     stocks = Stock.query.filter(Stock.ticker.like("%" + term + "%")).all()
#     return jsonify([stock.ticker for stock in stocks[:4]])
