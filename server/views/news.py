from flask import Blueprint, jsonify
from types import SimpleNamespace
import requests
from bs4 import BeautifulSoup

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, validate

import pymongo
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs

from server.decorators import check_confirmed
from server.extensions import cache
from server.models import Portfolio
from server.mongo_db import mongo_db

bp = Blueprint("news", __name__, url_prefix="/api/news")


def make_cache_key(*args, **kwargs):
    return request.url


@bp.route("", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=60 * 60 * 2, key_prefix=make_cache_key)  # 2 hours cached
def get_news():
    current_identity = get_jwt_identity()
    portfolios = Portfolio.query.filter_by(user_id=current_identity).order_by(Portfolio.created_at.desc()).all()
    return jsonify([portfolio.json["name"] for portfolio in portfolios])


@bp.route("/scrape", methods=["GET"])
@jwt_required
@check_confirmed
@cache.cached(timeout=60 * 60 * 2, key_prefix=make_cache_key)  # 2 hours cached
@use_args({
    "symbols": fields.DelimitedList(fields.Str(), required=True),
}, location="query")
def scrape_news(args):
    data = []
    for symbol in args["symbols"]:
        url = f"https://www.wsj.com/market-data/quotes/{symbol}"
        headers = {"User-Agent": "Twitterbot"}
        r = requests.get(url, headers=headers)
        news = BeautifulSoup(r.text, "html.parser")
        articles = news.find_all("li", attrs={"class": "cr_pressRelease"})
        for article in articles:
            date = article.find(attrs={"class": "cr_dateStamp"}).text
            provider = article.find(attrs={"class": "cr_provider"}).text
            headline = article.find(attrs={"class": "headline"})
            link = headline.a["href"]
            obj = {
                "symbol": symbol,
                "date_posted": date,
                "provider": provider,
                "headline": headline.a.text,
                "link": link,
            }
            data.append(obj)

    # tickers_collection = pymongo.collection.Collection(mongo_db, "news")
    return jsonify(data)
