import logging

import yfinance as yf
import json
from server.extensions import db
from server.models import Stock
import pandas as pd

log = logging.getLogger(__name__)

EMPTY_HISTORY_COLUMNS = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]


def fetch_stock_history(
    tickers, period="1y", interval="1d", start=None, end=None, include_info=False
):
    res = {}
    for ticker in tickers:
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
        except Exception:
            # Yahoo Finance rate-limits/blocks unpredictably (varies by
            # source IP); one flaky ticker shouldn't 500 the whole batch.
            log.exception("Failed to fetch history for ticker %s", ticker)
            history_json = {column: {} for column in EMPTY_HISTORY_COLUMNS}
        res[ticker] = history_json
    return res


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
