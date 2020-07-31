import os

from dotenv import load_dotenv
from flask import Flask, jsonify

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
    from application.extensions import migrate
    from application.extensions import mail
    from application.extensions import babel
    from application.extensions import cors
    from application.extensions import jwt

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    babel.init_app(app)
    cors.init_app(app,
                  resources={r"/api/*": {"origins": ["http://localhost:5000", "http://localhost:8080", "*"]}},
                  supports_credentials=True)
    jwt.init_app(app)

    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        messages = err.data.get("messages", "Invalid request.")
        return jsonify({"message": messages["json"]}), 400


def register_blueprints(app):
    from application.views import blueprints

    for blueprint in blueprints:
        app.register_blueprint(blueprint.bp)
