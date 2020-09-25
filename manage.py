import click

from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from server.common.common import slugify_keys
from server.extensions import db
from server.models import User, Role
from wsgi import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0"))
manager.add_command("db", MigrateCommand)


@manager.command
def create_user():
    email = click.prompt("Email")
    first_name = click.prompt("First name")
    last_name = click.prompt("Last name")
    password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
    role = click.prompt("Role")

    try:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            confirmed=True,
            email_confirmed_at=datetime.utcnow(),
        )
        role = Role(name=role)
        user.roles.append(role)
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


@manager.command
def populate_tickers():
    """
    Populate mongo db collection with all the symbols
    This will be done only once (or more if needed)
    I'm doing this due to limited API calls on free IEX account,
    and also to save some space in my Heroku postgresql DB, since they have limit of 10k rows for the DB :(
    """
    import pymongo
    from pymongo import TEXT
    from server.mongo_db import mongo_db
    from server.apis.iex import IEXFinance

    tickers_collection = pymongo.collection.Collection(mongo_db, "tickers")
    tickers_collection.drop()  # drop old data to repopulate it with fresh data

    tickers = IEXFinance.list_symbols()
    tickers_collection.insert_many([ticker for ticker in tickers])
    indexes = tickers_collection.list_indexes()
    if "SymbolIndex" in indexes:
        print("Done! Index already present.")
        return
    tickers_collection.create_index(
        [
            ("symbol", TEXT),
            ("name", TEXT),
        ],
        weights={"symbol": 20, "name": 1},
        name="SymbolIndex",
    )

    print("Done!")


@manager.command
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
            if not stock.ticker.upper() == k.upper():
                continue
            stock.company_info = slugify_keys(v["company_info"])
            stock.latest_market_data = slugify_keys(list(v.values())[0])
            db.session.commit()
            print(f"{stock.ticker} updated")

    print(
        f"Stock update finished, elapsed time: {round(time.time() - start_time, 2)} seconds"
    )


if __name__ == "__main__":
    manager.run()
