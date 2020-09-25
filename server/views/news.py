from bs4 import BeautifulSoup

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request, current_app
from webargs import fields
from webargs.flaskparser import use_args
from server.apis.nasdaq import Nasdaq
from server.decorators import check_confirmed
from server.extensions import cache
from server.models import Portfolio

bp = Blueprint("news", __name__, url_prefix="/api/news")


def make_cache_key(*args, **kwargs):
    return request.url


@bp.route("", methods=["GET"])
@jwt_required
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
@jwt_required
@check_confirmed
@cache.cached(timeout=60 * 60 * 2, key_prefix=make_cache_key)  # 2 hours cached
@use_args(
    {
        "symbols": fields.DelimitedList(fields.Str(), required=True),
    },
    location="query",
)
def scrape_news(args):
    data = []
    for symbol in args["symbols"]:
        r = Nasdaq.get_headlines(symbol)
        news = BeautifulSoup(r.text, "html.parser")
        articles = news.find_all(class_="quote-news-headlines__item")
        for article in articles:
            date = article.find(class_="quote-news-headlines__date").text
            provider = "Press release"  # TODO: remove this
            headline = article.find(class_="quote-news-headlines__item-title").span.text
            link = article.a["href"]
            obj = {
                "symbol": symbol,
                "date_posted": date,
                "provider": provider,
                "headline": headline,
                "link": f"{current_app.config.get('NASDAQ_API_URL')}{link}",
            }
            data.append(obj)

    # tickers_collection = pymongo.collection.Collection(mongo_db, "news")
    sort_by_symbol = sorted(data, key=lambda k: k["symbol"])
    return jsonify(sort_by_symbol)
