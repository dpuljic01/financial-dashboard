from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, validate
from server.decorators import check_confirmed
from server.models import User, Portfolio, Holding, Stock
from server.extensions import db
from webargs.flaskparser import use_kwargs
from types import SimpleNamespace

bp = Blueprint("profile", __name__, url_prefix="/api/users/self")


@bp.route("", methods=["GET"])
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
    portfolios = Portfolio.query.filter_by(user_id=current_identity).order_by(Portfolio.created_at.desc()).all()
    return jsonify([portfolio.json["name"] for portfolio in portfolios])


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
    "name": fields.String(required=True, validate=validate.Length(min=1, max=255)),
    "info": fields.String(),
})
def create_portfolio(**payload):
    current_identity = get_jwt_identity()

    portfolio = Portfolio.query.filter_by(name=payload["name"]).first()
    if portfolio:
        return jsonify({"message": "Portfolio with that name already exists."}), 409

    portfolio = Portfolio(name=payload["name"], user_id=current_identity, info=payload["info"])
    db.session.add(portfolio)
    db.session.commit()
    return jsonify(portfolio.json), 201


@bp.route("/holdings", methods=["POST"])
@jwt_required
@check_confirmed
@use_kwargs({
    "portfolio": fields.String(required=True),
    "symbol": fields.String(required=True),
    "price": fields.Decimal(required=True),
    "purchased_at": fields.DateTime(required=True),
})
def create_portfolio_holding(**payload):
    current_identity = get_jwt_identity()

    portfolio = Portfolio.query.filter_by(name=payload["portfolio"], user_id=current_identity).first()
    if not portfolio:
        return jsonify({"message": "Portfolio not found"}), 404

    # here call actual api to fetch company details based on symbol
    stock = SimpleNamespace(  # mocked!
        symbol="AAPL", 
        company_name="Apple Inc.", 
        company_details={"CEO": "Domagoj Puljic", "Exchange": "NYSE", "Price": 456.43}
    )

    stock_db = Stock(
        ticker = stock.symbol,
        short_name = stock.company_name,   
        info = stock.company_details,
    )
    db.session.add(stock_db)
    db.session.flush()

    holding_db = Holding(
        portfolio_id = portfolio.id,
        stock_id = stock_db.id,
        price = payload["price"],
        purchased_at = payload["purchased_at"],
    )
    db.session.add(holding_db)
    db.session.commit()
    return jsonify(portfolio.json), 201


@bp.route("/symbols", methods=["POST"])
@jwt_required
@check_confirmed
@use_kwargs({
    "portfolio": fields.String(required=True),
    "symbol": fields.String(required=True),
    "short_name": fields.String(),
})
def add_symbol():
    current_identity = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(user_id=current_identity, name=portfolio).first_or_404()
    stock_db = Stock(
        ticker = payload["symbol"],
        short_name = payload["short_name"],   
    )
    db.session.add(stock_db)
    db.session.commit()