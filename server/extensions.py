import os
from sqlalchemy import MetaData
from flask_babelex import Babel
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_caching import Cache
from flask_compress import Compress

from server.helpers.blacklist_tokens import BlacklistTokens

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()
mail = Mail()
babel = Babel()
cors = CORS()
jwt = JWTManager()
cache = Cache()
compress = Compress()


@jwt.unauthorized_loader  # override default "msg" key to be "message"
def my_expired_token_callback(unauthorized):
    return jsonify({"message": unauthorized}), 401


@jwt.expired_token_loader
def my_expired_token_callback(expired):
    return jsonify({"message": expired}), 401


@jwt.invalid_token_loader
def my_expired_token_callback(invalid):
    return jsonify({"message": invalid}), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return BlacklistTokens.check_revoked(decrypted_token)
