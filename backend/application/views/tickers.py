from flask import Blueprint, request, jsonify
from application.models import Stock


bp = Blueprint("tickers", __name__, url_prefix="/tickers")


@bp.route("/", methods=["POST"])
def add_holding():
    pass


@bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    term = request.args.get("q").upper()
    stocks = Stock.query.filter(Stock.ticker.like("%" + term + "%")).all()
    return jsonify([stock.ticker for stock in stocks[:4]])
