from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from server.decorators import check_confirmed
from server.models import User
from server.extensions import db

bp = Blueprint("profile", __name__, url_prefix="/api/users/self")


@bp.route("", methods=["GET"])
@jwt_required()
@check_confirmed  # this absolutely **must** come after @jwt_required decorator
def get_user():
    current_identity = get_jwt_identity()
    user = User.query.get_or_404(current_identity)
    return jsonify(user.json)


@bp.route("", methods=["PUT"])
@jwt_required()
@check_confirmed  # this absolutely **must** come after @jwt_required decorator
@use_kwargs(
    {
        "first_name": fields.Str(
            required=False, validate=validate.Length(min=1, max=255)
        ),
        "last_name": fields.Str(
            required=False, validate=validate.Length(min=1, max=255)
        ),
    }
)
def update_user(**kwargs):
    current_identity = get_jwt_identity()
    user = User.query.get_or_404(current_identity)
    if "first_name" in kwargs:
        user.first_name = kwargs["first_name"]
    if "last_name" in kwargs:
        user.last_name = kwargs["last_name"]
    db.session.commit()
    return jsonify(user.json)


@bp.route("/change-password", methods=["PUT"])
@jwt_required()
@check_confirmed  # this absolutely **must** come after @jwt_required decorator
@use_kwargs(
    {
        "old": fields.Str(required=True),
        "new": fields.Str(required=True, validate=validate.Length(min=8, max=255)),
    }
)
def change_password(**kwargs):
    current_identity = get_jwt_identity()
    user = User.query.get_or_404(current_identity)

    if kwargs["old"] != user.password:
        return jsonify({"message": "Invalid password"}), 400

    user.password = kwargs["new"]
    db.session.commit()
    return jsonify(), 204
