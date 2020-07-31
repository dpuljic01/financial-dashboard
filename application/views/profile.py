from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, validate
from application.decorators import check_confirmed
from application.models import User, Portfolio
from application.extensions import db
from webargs.flaskparser import use_kwargs

bp = Blueprint("profile", __name__, url_prefix="/api/users/self")


@bp.route("/")
@jwt_required
@check_confirmed  # this absolutely **must** come after @jwt_required decorator
def get_user():
    current_identity = get_jwt_identity()
    user = User.query.get_or_404(current_identity)
    return jsonify(user.json)


@bp.route("/portfolios", methods=["GET"])
@jwt_required
@check_confirmed
def list_portfolios():
    current_identity = get_jwt_identity()
    portfolios = Portfolio.query.filter_by(user_id=current_identity).all()
    return jsonify([portfolio.json for portfolio in portfolios])


@bp.route("/portfolios/<string:name>", methods=["GET"])
@jwt_required
@check_confirmed
def get_portfolio(name):
    current_identity = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(user_id=current_identity, name=name).first_or_404()
    return jsonify(portfolio.json)


@bp.route("/portfolios", methods=["POST"])
@jwt_required
@check_confirmed
@use_kwargs({
    "name": fields.String(required=True, validate=validate.Length(min=1, max=255))
})
def create_portfolio(**payload):
    current_identity = get_jwt_identity()

    portfolio = Portfolio.query.filter_by(name=payload["name"]).first()
    if portfolio:
        jsonify({"message": "Portfolio with that name already exists."}), 409

    portfolio = Portfolio(name=payload["name"], user_id=current_identity)
    db.session.add(portfolio)
    db.session.commit()
    return jsonify(portfolio.json), 201
