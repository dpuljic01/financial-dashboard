import yfinance as yf
import json
from server.extensions import db
from server.models import Stock
import pandas_datareader as pdr
import pandas as pd


def fetch_stock_history(tickers, period="1y", interval="1d", start=None, end=None, include_info=False):
    res = {}
    for ticker in tickers:
        data = yf.Ticker(ticker)
        history = data.history(period=period, interval=interval, start=start, end=end, group_by="ticker")
        history = history[~history.index.duplicated(keep="last")]
        history_json = json.loads(history.to_json(orient="columns", date_format="iso"))
        if include_info:
            try:
                history_json["company_info"] = data.get_info()
            except:
                pass
        res[ticker] = history_json
    return res


def create_stock(ticker):
    data = yf.Ticker(ticker)
    stock = Stock(
        ticker=ticker,
        short_name=data.info["shortName"],
        info=data.info
    )
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


def get_quote(ticker):
    data = pdr.get_quote_yahoo(ticker)
    return json.loads(data.to_json(orient="index"))
