from flask import jsonify
from flask_babel import Babel
from flask_caching import Cache
from flask_compress import Compress
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

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
def my_unauthorized_callback(reason):
    return jsonify({"message": reason}), 401


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired"}), 401


@jwt.invalid_token_loader
def my_invalid_token_callback(reason):
    return jsonify({"message": reason}), 401


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return BlacklistTokens.check_revoked(jwt_payload)
