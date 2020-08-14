import yfinance as yf
import json

from server.extensions import db
# from server.models import StockHistory
from server.models import Stock
from server.apis.iex import IEXFinance


# probably not a smart idea to save this into DB due to database limits on Heroku free account :(
# but I might be able to use Mongo Atlas to save only ones which user searches for.
def fetch_stock_history(tickers, period="1y", interval="1d", start=None, end=None):  # insert_into_db=False):
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
        res[ticker] = json.loads(history.to_json(orient="index"))

    return res

    # probably delete this below
    # objects = []
    # stock = create_stock(ticker)
    # for idx_h, row_h in history.iterrows():
    #     stock_history = StockHistory(
    #         stock_id=stock["id"],
    #         date=idx_h,
    #         close=row_h["Close"],
    #         open=row_h["Open"],
    #         high=row_h["High"],
    #         low=row_h["Low"],
    #         dividends=row_h["Dividends"],
    #         volume=row_h["Volume"]
    #     )
    #     objects.append(stock_history)
    #
    # try:
    #     db.session.bulk_save_objects(objects)
    #     db.session.commit()
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return
    # print("Done!")


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