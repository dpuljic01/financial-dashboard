import os

from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()


def create_app():
    app = Flask(__name__, static_folder='./../dist/static')

    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    from server.extensions import db
    from server.extensions import migrate
    from server.extensions import mail
    from server.extensions import babel
    from server.extensions import cors
    from server.extensions import jwt

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    babel.init_app(app)

    cors.init_app(app,
                  resources={r"/api/*": {"origins": "*"}},
                  supports_credentials=True)
    jwt.init_app(app)

    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        messages = err.data.get("messages", "Invalid request.")
        return jsonify({"message": messages["json"]}), 400


def register_blueprints(app):
    from server.views import blueprints
    from server.client import client_bp

    for blueprint in blueprints:
        app.register_blueprint(blueprint.bp)
    app.register_blueprint(client_bp)
