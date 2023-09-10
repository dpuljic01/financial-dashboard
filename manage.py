from datetime import datetime

import click
from flask.cli import FlaskGroup, with_appcontext
from flask_migrate import Migrate

from server.common.common import slugify_keys
from server.extensions import db
from wsgi import app

migrate = Migrate(app, db)
cli = FlaskGroup(app)


@cli.command("runserver", short_help="Run the development server.")
def runserver():
    """Run the development server."""
    if __name__ == "__main__":
        app.run(host="0.0.0.0")


@cli.command("create_user", short_help="Create a new user.")
@click.option("--email", prompt="Email")
@click.option("--first_name", prompt="First name")
@click.option("--last_name", prompt="Last name")
@click.option("--password", prompt="Password", hide_input=True, confirmation_prompt=True)
@click.option("--role", prompt="Role")
@with_appcontext
def create_user(email, first_name, last_name, password, role):
    """Create a new user."""
    from server.models import User
    try:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            confirmed=True,
            email_confirmed_at=datetime.utcnow(),
            role=role,
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")


# @manager.command
# def populate_stocks():
#     import yfinance as yf
#     from pandas_datareader import data as pdr
#     from server.models import Stock
#
#     yf.pdr_override()  # override pandas default source for yahoo data with our yfinance data source
#     df = pdr.get_nasdaq_symbols()
#     objects = []
#     for idx_s, row_s in df.iterrows():
#         if "$" in idx_s or "." in idx_s or len(str(idx_s)) > 5:  # skip just to have less data in DB, due to limits :/
#             continue
#
#         stock = Stock(ticker=idx_s, short_name=row_s["Security Name"])
#         objects.append(stock)
#
#     try:
#         db.session.bulk_save_objects(objects)
#         db.session.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         return
#     print("Done!")


@cli.command("populate_tickers", short_help="Populate MongoDB collection with symbols.")
@click.option("--force", is_flag=True, help="Force repopulation.")
@with_appcontext
def populate_tickers(force=False):
    """
    Populate mongo db collection with all the symbols
    This will be done only once (or more if needed)
    I'm doing this due to limited API calls on free IEX account,
    and also to save some space in my Heroku postgresql DB, since they have limit of 10k rows for the DB :(
    """
    import pymongo
    from server.mongo_db import mongo_db
    from server.apis.iex import IEXFinance

    tickers_collection = pymongo.collection.Collection(mongo_db, "tickers")
    if not force:
        indexes = tickers_collection.list_indexes()
        if "SymbolIndex" in indexes:
            print("Done! Index already present.")
            return

    tickers_collection.drop()  # Drop old data to repopulate it with fresh data

    tickers = IEXFinance.list_symbols()
    tickers_collection.insert_many([ticker for ticker in tickers])

    tickers_collection.create_index(
        [
            ("symbol", pymongo.TEXT),
            ("name", pymongo.TEXT),
        ],
        weights={"symbol": 20, "name": 1},
        name="SymbolIndex",
    )

    print("Done!")


@cli.command("update_stocks", short_help="Update stock information.")
@with_appcontext
def update_stocks():
    import time
    from server.models import Stock
    from server.apis.yfinance import fetch_stock_history

    print("Updating stock information ...")

    start_time = time.time()
    stocks = Stock.query.all()
    tickers = [stock.ticker for stock in stocks]
    stocks_data = fetch_stock_history(
        tickers=tickers, period="2d", interval="1d", include_info=True
    )
    print("Fetched new information ...")
    for k, v in stocks_data.items():
        for stock in stocks:
            if stock.ticker.upper() != k.upper():
                continue
            stock.company_info = slugify_keys(v["company_info"])
            stock.latest_market_data = slugify_keys(list(v.values())[0])
            db.session.commit()
            print(f"{stock.ticker} updated")

    print(
        f"Stock update finished, elapsed time: {round(time.time() - start_time, 2)} seconds"
    )
