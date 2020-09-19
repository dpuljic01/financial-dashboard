import requests
import re, time
from bs4 import BeautifulSoup

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args

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
        base_url = "https://www.nasdaq.com"
        url = f"{base_url}/market-activity/stocks/{symbol}/press-releases"
        headers = {"User-Agent": "*"}
        r = requests.get(url, headers=headers)
        news = BeautifulSoup(r.text, "html.parser")
        articles = news.find(class_="quote-press-release__list")
        for article in articles.find_all(class_="quote-press-release__card")[:4]:  # just first 4 is enough
            date = article.find(class_="quote-press-release__card-timestamp").text
            provider = "Press release"
            headline = article.find(class_="quote-press-release__card-title")
            link = headline.a["href"]
            obj = {
                "symbol": symbol,
                "date_posted": date,
                "provider": provider,
                "headline": headline.a.span.text,
                "link": f"{base_url}{link}",
            }
            data.append(obj)

    # tickers_collection = pymongo.collection.Collection(mongo_db, "news")
    sort_by_symbol = sorted(data, key=lambda k: k["symbol"])
    return jsonify(sort_by_symbol)
