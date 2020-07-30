from flask_babelex import Babel
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify

from application.helpers.blacklist_tokens import BlacklistTokens

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
babel = Babel()
cors = CORS()
jwt = JWTManager()


@jwt.unauthorized_loader  # override default "msg" key to be "message"
def my_expired_token_callback(unauthorized):
    return jsonify({'message': unauthorized}), 401


@jwt.expired_token_loader
def my_expired_token_callback(expired):
    return jsonify({'message': expired}), 401


@jwt.invalid_token_loader
def my_expired_token_callback(invalid):
    return jsonify({'message': invalid}), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return BlacklistTokens.check_revoked(decrypted_token)
