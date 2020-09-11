from urllib.parse import urljoin
from flask import current_app
import requests


class IEXUrl:
    def __init__(self, root):
        self.root = root

    def make(self, *args):
        return urljoin(self.root, *args)

    def quote(self, symbol=None, field=None):
        if not symbol:
            raise Exception("Symbol is required")
        return (
            self.make(f"/v1/stock/{symbol}/quote/{field}")
            if field
            else self.make(f"/v1/stock/{symbol}/quote")
        )

    def symbols(self):
        return self.make("/v1/ref-data/symbols")

    def search(self, symbol):
        if not symbol:
            raise Exception("Symbol is required")
        return self.make(f"/v1/search/{symbol}")

    def recommendations(self, symbol):
        if not symbol:
            raise Exception("Symbol is required")
        return self.make(f"/v1/stock/{symbol}/recommendation-trends")


class IEXFinanceApi:
    def __init__(self):
        self._token = None
        self._url = None

    def get(
        self, url, **kwargs
    ):  # probably move all these into separate file and inherit from it
        return requests.get(url, **kwargs)

    def post(self, url, **kwargs):
        return requests.post(url, **kwargs)

    def put(self, url, **kwargs):
        return requests.put(url, **kwargs)

    def delete(self, url, **kwargs):
        return requests.delete(url, **kwargs)

    @property
    def token(self):
        if self._token is None:
            self._token = current_app.config.get("IEX_TOKEN")
        return self._token

    @property
    def url(self):
        if self._url is None:
            self._url = IEXUrl(current_app.config.get("IEX_BASE_URL"))
        return self._url

    def get_stock_quote(self, ticker):
        resp = requests.get(self.url.quote(str(ticker)), params={"token": self.token})
        resp.raise_for_status()
        return resp.json()

    def list_symbols(self):
        resp = requests.get(self.url.symbols(), params={"token": self.token})
        resp.raise_for_status()
        return resp.json()

    def search(self, q):
        resp = requests.get(self.url.search(q), params={"token": self.token})
        resp.raise_for_status()
        return resp.json()

    def get_recommendations(self, symbol):
        resp = requests.get(
            self.url.recommendations(symbol), params={"token": self.token}
        )
        resp.raise_for_status()
        return resp.json()


IEXFinance = IEXFinanceApi()
