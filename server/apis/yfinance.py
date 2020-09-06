import yfinance as yf
import json
import datetime
from server.extensions import db
from server.models import Stock
import pandas_datareader as pdr
import pandas as pd


# probably not a smart idea to save this into DB due to database limits on Heroku free account :(
# but I might be able to use Mongo Atlas to save only ones which user searches for.
def fetch_stock_history(tickers, period="1y", interval="1d", start=None, end=None, include_info=False):  # insert_into_db=False):
    res = {}

    for ticker in tickers:
        data = yf.Ticker(ticker)
        # data = yf.download(
        #     tickers=ticker,
        #     period=period,
        #     interval=interval,
        #     group_by="ticker",
        #     threads=True,
        # )
        # name = data.info
        # iex = IEXFinance.get_stock_quote(ticker)
        # print(iex)
        history = data.history(period=period, interval=interval, start=start, end=end)
        history = history[~history.index.duplicated(keep="last")]
        history_json = history.to_json(orient="index", date_format="iso")
        res[ticker] = json.loads(history_json)
        if include_info:
            try:
                res[ticker]["company_info"] = data.get_info()
            except:
                pass

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
