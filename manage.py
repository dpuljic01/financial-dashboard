import click

from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

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
            email_confirmed_at=datetime.utcnow()
        )
        role = Role(name=role)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")


@manager.command
def populate_stocks():
    import yfinance as yf
    from pandas_datareader import data as pdr
    from server.models import Stock

    yf.pdr_override()  # override pandas default source for yahoo data with our yfinance data source
    df = pdr.get_nasdaq_symbols()
    objects = []
    for idx_s, row_s in df.iterrows():
        if "$" in idx_s or "." in idx_s or len(str(idx_s)) > 5:  # skip just to have less data in DB, due to limits :/
            continue

        stock = Stock(ticker=idx_s, short_name=row_s["Security Name"])
        objects.append(stock)

    try:
        db.session.bulk_save_objects(objects)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
        return
    print("Done!")


if __name__ == "__main__":
    manager.run()
