import yfinance as yf
import json
from server.extensions import db
from server.models import Stock
import pandas as pd


def fetch_stock_history(
    tickers, period="1y", interval="1d", start=None, end=None, include_info=False
):
    res = {}
    for ticker in tickers:
        data = yf.Ticker(ticker)
        history = data.history(
            period=period, interval=interval, start=start, end=end, group_by="ticker"
        )
        history = history[~history.index.duplicated(keep="last")]
        history_json = json.loads(history.to_json(orient="columns", date_format="iso"))
        if include_info:
            try:
                history_json["company_info"] = data.info
            except Exception:
                pass
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
    """Return a minimal quote dict for ticker using yfinance fast_info."""
    try:
        t = yf.Ticker(ticker)
        fi = t.fast_info
        return {
            ticker: {
                "symbol": ticker,
                "price": fi.last_price,
                "open": fi.open,
                "dayHigh": fi.day_high,
                "dayLow": fi.day_low,
                "volume": fi.three_month_average_volume,
                "marketCap": fi.market_cap,
                "fiftyTwoWeekHigh": fi.fifty_two_week_high,
                "fiftyTwoWeekLow": fi.fifty_two_week_low,
            }
        }
    except Exception:
        return {ticker: {}}
