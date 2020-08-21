from flask import Blueprint, jsonify
from types import SimpleNamespace

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import fields, validate
from webargs.flaskparser import use_kwargs

from server.apis.alpha_vantage import AlphaVantage
from server.apis.iex import IEXFinance
from server.apis.yfinance import fetch_stock_history
from server.decorators import check_confirmed
from server.extensions import db
from server.models import Portfolio, Holding, Stock

bp = Blueprint("portfolios", __name__, url_prefix="/api/portfolios")


@bp.route("", methods=["GET"])
@jwt_required
@check_confirmed
def list_portfolios():
    current_identity = get_jwt_identity()
    portfolios = Portfolio.query.filter_by(user_id=current_identity).order_by(Portfolio.created_at.desc()).all()
    return jsonify([portfolio.json["name"] for portfolio in portfolios])


@bp.route("/<string:name>", methods=["GET"])
@jwt_required
@check_confirmed
def get_portfolio(name):
    current_identity = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(user_id=current_identity, name=name).first_or_404()
    return jsonify(portfolio.json)


@bp.route("", methods=["POST"])
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


@bp.route("/<int:portfolio_id>", methods=["PUT"])
@jwt_required
@check_confirmed
@use_kwargs({
    "name": fields.String(),
    "info": fields.String(),
})
def update_portfolio(portfolio_id, **payload):
    current_identity = get_jwt_identity()

    portfolio_db = Portfolio.query.get_or_404(portfolio_id)
    portfolio = Portfolio.query.filter_by(name=payload["name"]).first()
    if portfolio:
        return jsonify({"message": "Portfolio with that name already exists."}), 409

    portfolio_db.update(payload)
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
        ticker=stock.symbol,
        short_name=stock.company_name,
        info=stock.company_details,
    )
    db.session.add(stock_db)
    db.session.flush()

    holding_db = Holding(
        portfolio_id=portfolio.id,
        stock_id=stock_db.id,
        price=payload["price"],
        purchased_at=payload["purchased_at"],
    )
    db.session.add(holding_db)
    db.session.commit()
    return jsonify(portfolio.json), 201


@bp.route("/<string:portfolio_name>/symbols", methods=["POST"])
@jwt_required
@check_confirmed
@use_kwargs({
    "symbol": fields.String(required=True),
    "short_name": fields.String(),
})
def add_symbol(portfolio_name, **payload):
    current_identity = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(user_id=current_identity, name=portfolio_name).first_or_404()

    stock_db = Stock.query.filter_by(ticker=payload["symbol"]).first()
    stock_in_portfolio = stock_db and (stock_db in portfolio.stocks)

    if stock_in_portfolio:
        return jsonify({"message": "Symbol already exists in this portfolio"}), 400
    elif stock_db:
        portfolio.stocks.append(stock_db)
        db.session.add(portfolio)
        db.session.commit()
        return jsonify(stock_db.json), 201

    # quote = IEXFinance.get_stock_quote(ticker=payload["symbol"])
    # if not quote:
    #     params = {"function": "GLOBAL_QUOTE", "symbol": payload["symbol"]}
    #     global_quote = AlphaVantage.fetch_data(params)
    #     if 'Note' in global_quote:
    #         print("AlphaVantage API limit exceeded")
    #         quote = {}
    #     else:
    #         quote = AlphaVantage.filter_global_quote(global_quote)
    data = fetch_stock_history(tickers=[payload["symbol"]], period="1d", interval="1d", include_info=True)
    vals = list(data[payload["symbol"]].values())

    stock_db = Stock(
        ticker=payload["symbol"],
        short_name=payload["short_name"],
        company_info=data[payload["symbol"]].get("company_info", {}),
        latest_market_data=vals[0]
    )
    portfolio.stocks.append(stock_db)
    db.session.add(portfolio)
    db.session.add(stock_db)
    db.session.commit()
    return jsonify(stock_db.json), 201
