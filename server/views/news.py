from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args
from server.apis.yfinance import get_stock_news
from server.decorators import check_confirmed
from server.extensions import cache
from server.models import Portfolio

bp = Blueprint("news", __name__, url_prefix="/api/news")


def make_cache_key(*args, **kwargs):
    return request.url


def _has_news_data(response):
    # Same rationale as tickers.py's history cache filter: a flaky/rate-
    # limited yfinance response shouldn't get cached empty for 2 hours.
    try:
        data = response.get_json()
    except Exception:
        return False
    return bool(data)


@bp.route("", methods=["GET"])
@jwt_required()
@check_confirmed
@cache.cached(timeout=60 * 60 * 2, key_prefix=make_cache_key)  # 2 hours cached
def get_news():
    current_identity = get_jwt_identity()
    portfolios = (
        Portfolio.query.filter_by(user_id=current_identity)
        .order_by(Portfolio.created_at.desc())
        .all()
    )
    return jsonify([portfolio.json["name"] for portfolio in portfolios])


@bp.route("/scrape", methods=["GET"])
@jwt_required()
@check_confirmed
@cache.cached(
    timeout=60 * 60 * 2, key_prefix=make_cache_key, response_filter=_has_news_data
)  # 2 hours cached
@use_args(
    {
        "symbols": fields.DelimitedList(fields.Str(), required=True),
    },
    location="query",
)
def scrape_news(args):
    data = []
    for symbol in args["symbols"]:
        data.extend(get_stock_news(symbol))

    sort_by_symbol = sorted(data, key=lambda k: k["symbol"])
    return jsonify(sort_by_symbol)
