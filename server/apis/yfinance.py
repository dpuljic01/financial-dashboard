import logging
from concurrent.futures import ThreadPoolExecutor

import yfinance as yf
import json
from server.extensions import db
from server.models import Stock
import pandas as pd

log = logging.getLogger(__name__)

EMPTY_HISTORY_COLUMNS = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
MAX_HISTORY_WORKERS = 8


def _fetch_one_ticker_history(ticker, period, interval, start, end, include_info):
    try:
        data = yf.Ticker(ticker)
        history = data.history(
            period=period, interval=interval, start=start, end=end
        )
        history = history[~history.index.duplicated(keep="last")]
        history_json = json.loads(
            history.to_json(orient="columns", date_format="iso")
        )
        if include_info:
            try:
                history_json["company_info"] = data.get_info()
            except Exception:
                pass
        return ticker, history_json
    except Exception:
        # Yahoo Finance rate-limits/blocks unpredictably (varies by
        # source IP); one flaky ticker shouldn't 500 the whole batch.
        log.exception("Failed to fetch history for ticker %s", ticker)
        return ticker, {column: {} for column in EMPTY_HISTORY_COLUMNS}


def fetch_stock_history(
    tickers, period="1y", interval="1d", start=None, end=None, include_info=False
):
    tickers = list(tickers)
    if len(tickers) <= 1:
        results = [
            _fetch_one_ticker_history(ticker, period, interval, start, end, include_info)
            for ticker in tickers
        ]
        return dict(results)

    # Each ticker is an independent network round-trip to Yahoo, so fetching
    # them concurrently turns an N-ticker request from N sequential
    # round-trips into roughly one (e.g. the 9-symbol market overview chart).
    with ThreadPoolExecutor(max_workers=min(len(tickers), MAX_HISTORY_WORKERS)) as executor:
        results = executor.map(
            lambda ticker: _fetch_one_ticker_history(
                ticker, period, interval, start, end, include_info
            ),
            tickers,
        )
        return dict(results)


def create_stock(ticker):
    data = yf.Ticker(ticker)
    stock = Stock(ticker=ticker, short_name=data.info["shortName"], info=data.info)
    db.session.add(stock)
    db.session.commit()
    return stock.json


def fetch_stock_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info


def get_stock_recommendations(ticker):
    stock = yf.Ticker(ticker)
    data = stock.recommendations
    if isinstance(data, pd.DataFrame):
        data = json.loads(data.to_json(orient="index"))
    return data


def fetch_institutional_holders(ticker):
    stock = yf.Ticker(ticker)
    return stock.institutional_holders


def fetch__stock_calendar(ticker):
    stock = yf.Ticker(ticker)
    return stock.calendar


def search_symbols(query, max_results=8):
    # Replaces the old MongoDB-backed ticker search (populated from IEX
    # Cloud, which shut down in 2024 and left that collection permanently
    # empty). yfinance's Search hits Yahoo's own search endpoint directly -
    # real, current results, no separate data source to maintain.
    try:
        results = yf.Search(query, max_results=max_results).quotes
    except Exception:
        log.exception("Failed to search symbols for query %s", query)
        return []
    return [
        {
            "symbol": item["symbol"],
            "name": item.get("shortname") or item.get("longname") or item["symbol"],
        }
        for item in results
        if item.get("symbol")
    ]


def get_stock_news(ticker, max_results=8):
    # Replaces the old Nasdaq HTML-scraping approach (nasdaq.com's
    # news-headlines-fetcher endpoint now just serves a "Maintenance" page,
    # so BeautifulSoup always found zero matching elements). yfinance's
    # own .news surfaces Yahoo Finance's article feed directly.
    try:
        items = yf.Ticker(ticker).news or []
    except Exception:
        log.exception("Failed to fetch news for ticker %s", ticker)
        return []
    articles = []
    for item in items[:max_results]:
        content = item.get("content") or {}
        title = content.get("title")
        link = (content.get("canonicalUrl") or content.get("clickThroughUrl") or {}).get("url")
        if not title or not link:
            continue
        provider = (content.get("provider") or {}).get("displayName") or "Yahoo Finance"
        articles.append(
            {
                "symbol": ticker,
                "headline": title,
                "date_posted": content.get("pubDate", ""),
                "provider": provider,
                "link": link,
            }
        )
    return articles


def _get_one_quote(ticker):
    try:
        return ticker, get_quote(ticker)[ticker]
    except Exception:
        log.exception("Failed to fetch quote for ticker %s", ticker)
        return ticker, None


def get_market_snapshot(tickers):
    # Used by the public landing page ticker tape - lightweight quotes only
    # (no history), for a small fixed set of indices/commodities/FX.
    with ThreadPoolExecutor(max_workers=min(len(tickers), MAX_HISTORY_WORKERS)) as executor:
        results = executor.map(_get_one_quote, tickers)
        return {ticker: quote for ticker, quote in results if quote}


def get_quote(ticker):
    # pandas_datareader's get_quote_yahoo hits a Yahoo endpoint that's been
    # broken for years (hangs/errors unpredictably); fast_info is yfinance's
    # own lightweight quote data and is reliable. Key names mirror the old
    # regularMarket* fields from Yahoo's quote API so slugify_keys() (which
    # strips the "regularMarket" prefix) keeps producing the same
    # price/changepercent/volume keys the frontend already expects.
    info = yf.Ticker(ticker).fast_info
    price = info.last_price
    previous_close = info.previous_close
    change_percent = (
        (price - previous_close) / previous_close * 100 if previous_close else None
    )
    return {
        ticker: {
            "regularMarketPrice": price,
            "regularMarketChangePercent": change_percent,
            "regularMarketVolume": info.last_volume,
        }
    }
