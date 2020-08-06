from datetime import datetime

from flask import Blueprint, jsonify, current_app
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from server.email import send_password_reset_email, send_verify_email
from server.extensions import db
from server.models import User
from server.token import generate_confirmation_token, confirm_token
from flask_jwt_extended import (
    create_access_token, get_jti, get_jwt_identity, jwt_required, get_raw_jwt
)
from server.helpers.blacklist_tokens import BlacklistTokens

bp = Blueprint("auth", __name__, url_prefix="/api")


@bp.route("/session/auth", methods=["POST"])
@use_kwargs({
    "email": fields.Str(required=True, validate=validate.Email()),
    "password": fields.Str(required=True),
})
def login(**payload):
    db_user = User.auth(email=payload["email"], password=payload["password"])

    if not db_user or not db_user.confirmed:
        return jsonify({"message": "Invalid credentials", "authenticated": False, "confirmed": False}), 401

    # Create JWT
    access_token = create_access_token(identity=db_user.id)
    # refresh_token = create_refresh_token(identity=db_user.id)

    # Store the tokens in redis with a status of not currently revoked. We
    # can use the `get_jti()` method to get the unique identifier string for
    # each token. We can also set an expires time on these tokens in redis,
    # so they will get automatically removed after they expire. We will set
    # everything to be automatically removed shortly after the token expires

    db_user.last_logged_in = datetime.utcnow()
    db.session.commit()

    try:
        access_jti = get_jti(encoded_token=access_token)
        BlacklistTokens.revoked_store.set(access_jti, "false", current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] * 1.1)
    except:
        pass

    return jsonify({"access_token": access_token}), 200


# Endpoint for revoking the current users access token
@bp.route("/session/revoke", methods=["DELETE"])
@jwt_required
def logout():
    try:
        jti = get_raw_jwt()["jti"]
        BlacklistTokens.revoked_store.set(jti, "true", current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] * 1.1)
    except:
        pass

    return "", 204


@bp.route("/register", methods=["POST"])
@use_kwargs({
    "first_name": fields.Str(required=True, validate=validate.Length(min=1, max=255)),
    "last_name": fields.Str(required=True, validate=validate.Length(min=1, max=255)),
    "email": fields.Email(required=True)
})
def register(**payload):
    db_user = User.query.filter_by(email=payload["email"]).first()
    if db_user:
        return jsonify({"message": "Email already exists."}), 409

    db_user = User(
        first_name=payload["first_name"],
        last_name=payload["last_name"],
        email=payload["email"],
    )

    # add the new user to the database
    db.session.add(db_user)
    db.session.commit()

    token = generate_confirmation_token(db_user.email)
    send_verify_email(
        fe_url=current_app.config.get('FINANCIAL_DASHBOARD_FE_URL'),
        email=db_user.email,
        token=token
    )

    return jsonify(db_user.json), 201


@bp.route("/unconfirmed", methods=["GET"])
@jwt_required
def unconfirmed():
    current_identity = get_jwt_identity()
    db_user = User.query.get_or_404(current_identity)
    if not db_user.confirmed:
        return jsonify({"message": "Invalid credentials", "authenticated": True, "confirmed": False}), 403
    return jsonify({"message": "User confirmed.", "authenticated": True, "confirmed": True}), 200


@bp.route("/reset-password", methods=["POST"])
@use_kwargs({
    "email": fields.String(required=True, validate=validate.Email())
})
def reset(**payload):
    db_user = User.query.filter_by(email=payload["email"]).first_or_404()

    token = generate_confirmation_token(db_user.email)
    send_password_reset_email(
        fe_url=current_app.config.get('FINANCIAL_DASHBOARD_FE_URL'),
        email=db_user.email,
        token=token
    )

    return "", 204


@bp.route("/reset-password", methods=["PUT"])
@use_kwargs({
    "token": fields.String(required=True),
    "password": fields.String(required=True, validate=[validate.Length(min=8, max=255)])
})
def reset_password(**payload):
    email = confirm_token(payload["token"])

    if not email or email in [True, 1]:
        jsonify({"message": "Link is invalid or has expired."}), 400

    user = User.query.filter_by(email=email).first_or_404()
    user.password = payload["password"]

    if not user.confirmed:
        user.confirmed = True
        user.email_confirmed_at = datetime.utcnow()

    db.session.commit()

    return "", 204
