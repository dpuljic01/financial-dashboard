from urllib.parse import urljoin
from flask import current_app
from server.apis.base_api import BaseApi


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


class IEXFinanceApi(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)
        self._session = None
        self._token = None
        self._url = None

    @property
    def token(self):
        if self._token is None:
            self._token = current_app.config.get("IEX_TOKEN")
        return self._token

    @property
    def session(self):
        if self._session is None:
            self._session = BaseApi.create_session()
            self._session.params.update({"token": self.token})
        return self._session

    @property
    def url(self):
        if self._url is None:
            self._url = IEXUrl(current_app.config.get("IEX_BASE_URL"))
        return self._url

    def get_stock_quote(self, ticker):
        resp = self.get(self.url.quote(str(ticker)))
        resp.raise_for_status()
        return resp.json()

    def list_symbols(self):
        resp = self.get(self.url.symbols())
        resp.raise_for_status()
        return resp.json()

    def search(self, q):
        resp = self.get(self.url.search(q))
        resp.raise_for_status()
        return resp.json()

    def get_recommendations(self, symbol):
        resp = self.get(self.url.recommendations(symbol))
        resp.raise_for_status()
        return resp.json()


IEXFinance = IEXFinanceApi()
