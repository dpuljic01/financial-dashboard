import yfinance as yf

from server.extensions import db
from server.models import StockHistory
from server.models import Stock


# probably not a smart idea to save this into DB due to database limits on Heroku free account :(
def fetch_stock_history(ticker, period="1y", interval="1d", insert_into_db=False):
    data = yf.Ticker(ticker)
    history = data.history(period=period, interval=interval)

    if not insert_into_db:
        return history

    objects = []
    stock = create_stock(ticker)
    for idx_h, row_h in history.iterrows():
        stock_history = StockHistory(
            stock_id=stock["id"],
            date=idx_h,
            close=row_h["Close"],
            open=row_h["Open"],
            high=row_h["High"],
            low=row_h["Low"],
            dividends=row_h["Dividends"],
            volume=row_h["Volume"]
        )
        objects.append(stock_history)

    try:
        db.session.bulk_save_objects(objects)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        return
    print("Done!")


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
