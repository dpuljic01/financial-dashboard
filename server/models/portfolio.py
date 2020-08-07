from server.extensions import db
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import JSONB, UUID
from server.models.mixin import TimestampMixin


class Portfolio(db.Model, TimestampMixin):
    __tablename__ = "portfolio"

    id = db.Column(db.Integer(), db.Sequence("portfolio_id_seq"), primary_key=True)
    name = db.Column(db.String(50), nullable=True, server_default="Default")
    info = db.Column(db.Text())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", back_populates="portfolios")
    stocks = db.relationship("Stock", secondary="portfolio_stocks")
    purchases = db.relationship("Purchase", backref="portfolio", uselist=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def json(self):
        return {
            "name": self.name,
            "stocks": [stock.json for stock in self.stocks],
        }


class Stock(db.Model, TimestampMixin):
    __tablename__ = "stocks"

    id = db.Column(db.Integer(), db.Sequence("stocks_id_seq"), primary_key=True)
    ticker = db.Column(db.String(15), unique=True)
    short_name = db.Column(db.String(255))   
    info = db.Column(JSONB)

    history = db.relationship("StockHistory", backref="stock", uselist=True)

    @property
    def json(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "short_name": self.short_name,
            "info": self.info
        }


class Purchase(db.Model, TimestampMixin):  # all user purchases (which portfolio, which stock, at what price)
    id = db.Column(db.Integer(), db.Sequence("purchases_id_seq"), primary_key=True)
    portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolio.id", ondelete="CASCADE"), nullable=False)
    stock_id = db.Column(db.Integer(), db.ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    price = db.Column(Numeric, nullable=False)
    purchased_at = db.Column(db.DateTime(), nullable=False)

    @property
    def json(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "stock_id": self.stock_id,
            "price": self.price,
            "purchased_at": self.purchased_at,
        }


class StockHistory(db.Model):
    id = db.Column(db.Integer(), db.Sequence("stock_history_id_seq"), primary_key=True)
    stock_id = db.Column(db.Integer(), db.ForeignKey("stocks.id", ondelete="CASCADE"))
    date = db.Column(db.DateTime())
    close = db.Column(Numeric)
    open = db.Column(Numeric)
    high = db.Column(Numeric)
    low = db.Column(Numeric)
    dividends = db.Column(Numeric)
    volume = db.Column(Numeric)


class PortfolioStocks(db.Model):
    __tablename__ = "portfolio_stocks"

    id = db.Column(db.Integer(), primary_key=True)
    portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolio.id", ondelete="CASCADE"))
    stock_id = db.Column(db.Integer(), db.ForeignKey("stocks.id", ondelete="CASCADE"))
