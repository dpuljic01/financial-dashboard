from server.extensions import db
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import JSONB, UUID
from server.models.mixin import TimestampMixin
from sqlalchemy import (
    UniqueConstraint,
)


class Portfolio(db.Model, TimestampMixin):
    __tablename__ = "portfolio"

    id = db.Column(db.Integer(), db.Sequence("portfolio_id_seq"), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default="Default")
    info = db.Column(db.Text())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", back_populates="portfolios")
    stocks = db.relationship("Stock", secondary="portfolio_stocks", backref="portfolio")
    holdings = db.relationship("Holding", backref="portfolio", uselist=True)

    __table_args__ = (
        UniqueConstraint("name", "user_id", name="uq_portfolio_name_user_id"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "holdings": [holding.json for holding in self.holdings],
            "stocks": [stock.json for stock in self.stocks],
        }


class Stock(db.Model, TimestampMixin):
    __tablename__ = "stocks"

    id = db.Column(db.Integer(), db.Sequence("stocks_id_seq"), primary_key=True)
    ticker = db.Column(db.String(15))
    short_name = db.Column(db.String(255))
    latest_market_data = db.Column(JSONB)
    company_info = db.Column(JSONB)

    __table_args__ = (
        UniqueConstraint("ticker", name="uq_stocks_ticker"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def json(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "short_name": self.short_name,
            "company_info": self.company_info,
            "latest_market_data": self.latest_market_data
        }


class Holding(db.Model, TimestampMixin):  # all user holdings (which portfolio, which stock, at what price)
    __tablename__ = "holdings"

    id = db.Column(db.Integer(), db.Sequence("holdings_id_seq"), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolio.id", ondelete="CASCADE"), nullable=False)
    stock_id = db.Column(db.Integer(), db.ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    shares = db.Column(Numeric(asdecimal=False), nullable=False)
    price = db.Column(Numeric(asdecimal=False), nullable=False)
    purchased_at = db.Column(db.DateTime(), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "portfolio_id": self.portfolio_id,
            "stock_id": self.stock_id,
            "price": self.price,
            "purchased_at": self.purchased_at,
            "shares": self.shares,
        }


class PortfolioStocks(db.Model):
    __tablename__ = "portfolio_stocks"

    portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolio.id", ondelete="CASCADE"), primary_key=True)
    stock_id = db.Column(db.Integer(), db.ForeignKey("stocks.id", ondelete="CASCADE"), primary_key=True)
