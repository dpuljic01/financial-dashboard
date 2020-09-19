from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, validate
from webargs.flaskparser import use_kwargs
from datetime import datetime

from server.apis.yfinance import fetch_stock_info, get_quote
from server.common.common import lowercase_keys
from server.decorators import check_confirmed
from server.extensions import db
from server.models import Portfolio, Holding, Stock, PortfolioStocks

bp = Blueprint("portfolios", __name__, url_prefix="/api/portfolios")


@bp.route("", methods=["GET"])
@jwt_required
@check_confirmed
def list_portfolios():
    current_identity = get_jwt_identity()
    portfolios = (
        Portfolio.query.filter_by(user_id=current_identity)
        .order_by(Portfolio.created_at.desc())
        .all()
    )
    return jsonify([portfolio.json_short for portfolio in portfolios])


@bp.route("/<int:identifier>", methods=["GET"])
@jwt_required
@check_confirmed
def get_portfolio(identifier):
    current_identity = get_jwt_identity()
    if isinstance(identifier, int):
        portfolio = Portfolio.query.get_or_404(identifier)
    else:
        portfolio = Portfolio.query.filter_by(
            user_id=current_identity, name=identifier
        ).first_or_404()
    return jsonify(portfolio.json)


@bp.route("", methods=["POST"])
@jwt_required
@check_confirmed
@use_kwargs(
    {
        "name": fields.String(required=True, validate=validate.Length(min=1, max=255)),
        "info": fields.String(),
    }
)
def create_portfolio(**payload):
    current_identity = get_jwt_identity()

    portfolio = Portfolio.query.filter_by(
        name=payload["name"], user_id=current_identity
    ).first()
    if portfolio:
        return jsonify({"message": "Portfolio with that name already exists."}), 409

    portfolio = Portfolio(
        name=payload["name"], user_id=current_identity, info=payload["info"]
    )
    db.session.add(portfolio)
    db.session.commit()
    return jsonify(portfolio.json_short), 201


@bp.route("/<int:portfolio_id>", methods=["PUT"])
@jwt_required
@check_confirmed
@use_kwargs(
    {
        "name": fields.String(),
        "info": fields.String(),
    }
)
def update_portfolio(portfolio_id, **payload):
    current_identity = get_jwt_identity()
    portfolio_db = Portfolio.query.filter_by(
        id=portfolio_id, user_id=current_identity
    ).first_or_404()

    # portfolio = Portfolio.query.filter_by(name=payload["name"], user_id=current_identity).first()
    # if portfolio:
    #     return jsonify({"message": "Portfolio with that name already exists."}), 409

    portfolio_db.update(payload)
    db.session.commit()
    return jsonify(portfolio_db.json_short), 201


@bp.route("/<int:portfolio_id>", methods=["DELETE"])
@jwt_required
@check_confirmed
def delete_portfolio(portfolio_id):
    current_identity = get_jwt_identity()
    portfolio_db = Portfolio.query.filter_by(
        id=portfolio_id, user_id=current_identity
    ).first_or_404()
    db.session.delete(portfolio_db)
    db.session.commit()
    return jsonify(), 204


@bp.route("/<int:portfolio_id>/<int:stock_id>", methods=["DELETE"])
@jwt_required
@check_confirmed
def delete_portfolio_stock(portfolio_id, stock_id):
    current_identity = get_jwt_identity()
    portfolio_db = Portfolio.query.filter_by(
        id=portfolio_id, user_id=current_identity
    ).first_or_404()
    stock_db = None
    for stock in portfolio_db.stocks:
        if stock.id != stock_id:
            continue
        stock_db = stock

    if not stock_db:
        abort(404)

    db.session.delete(stock_db)
    db.session.commit()
    return jsonify(), 204


@bp.route("/<int:portfolio_id>/holdings", methods=["POST"])
@jwt_required
@check_confirmed
@use_kwargs(
    {
        "symbol": fields.String(required=True),
        "shares": fields.Decimal(required=True),
        "price": fields.Decimal(required=True),
        "purchased_at": fields.DateTime(required=False, missing=datetime.now()),
    }
)
def create_portfolio_holding(portfolio_id, **payload):
    current_identity = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(
        id=portfolio_id, user_id=current_identity
    ).first_or_404()

    symbol = payload["symbol"].upper()
    stock_db = Stock.query.filter_by(ticker=symbol).first_or_404()

    if stock_db not in portfolio.stocks:
        return jsonify({"message": "Symbol does not exist in current portfolio"})

    holding_db = Holding(
        portfolio_id=portfolio_id,
        user_id=current_identity,
        stock_id=stock_db.id,
        price=payload["price"],
        purchased_at=payload["purchased_at"],
        shares=payload["shares"],
    )
    db.session.add(holding_db)
    db.session.commit()
    return jsonify(holding_db.json), 201


@bp.route("/<int:holding_id>", methods=["DELETE"])
@jwt_required
@check_confirmed
def delete_portfolio_holding(holding_id):
    current_identity = get_jwt_identity()
    holding_db = Holding.query.filter_by(
        id=holding_id, user_id=current_identity
    ).first_or_404()
    db.session.delete(holding_db)
    db.session.commit()
    return jsonify(), 204


@bp.route("/<string:portfolio_id>/symbols", methods=["POST"])
@jwt_required
@check_confirmed
@use_kwargs(
    {
        "symbol": fields.String(required=True),
        "short_name": fields.String(),
    }
)
def add_symbol(portfolio_id, **payload):
    symbol = payload["symbol"].upper()

    current_identity = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(
        user_id=current_identity, id=portfolio_id
    ).first_or_404()

    stock_db = Stock.query.filter_by(ticker=symbol).first()
    stock_in_portfolio = stock_db and (stock_db in portfolio.stocks)

    if stock_in_portfolio:
        return jsonify({"message": "Symbol already exists in this portfolio"}), 400

    try:
        quote = get_quote(symbol)[symbol]
    except:
        quote = {}

    if stock_db:
        if quote:
            stock_db.latest_market_data = lowercase_keys(quote)
        portfolio.stocks.append(stock_db)
        db.session.commit()
        return jsonify(stock_db.json_short), 201

    stock_db = Stock(
        ticker=payload["symbol"],
        short_name=payload["short_name"],
        company_info={},
        latest_market_data=lowercase_keys(quote) if quote else {},
    )
    portfolio.stocks.append(stock_db)
    db.session.add(stock_db)
    db.session.commit()
    return jsonify(stock_db.json_short), 201
