import os

from dotenv import load_dotenv
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    from application.extensions import db
    from application.extensions import login
    from application.extensions import migrate
    from application.extensions import mail
    from application.extensions import babel
    from application.extensions import csrf

    csrf._exempt_views.add('dash.dash.dispatch')

    db.init_app(app)
    login.init_app(app)
    login.login_view = "auth.login"
    migrate.init_app(app, db)
    mail.init_app(app)
    babel.init_app(app)
    # csrf.init_app(app)


def register_blueprints(app):
    from application.views import blueprints

    for blueprint in blueprints:
        app.register_blueprint(blueprint.bp)
