from urllib.parse import urljoin
from flask import current_app
from server.apis.base_api import BaseApi


class NasdaqUrl:
    def __init__(self, root):
        self.root = root

    def make(self, *args):
        return urljoin(self.root, *args)

    def info(self, symbol):
        if not symbol:
            raise Exception("Symbol is required")
        return self.make(f"/api/quote/{symbol.upper()}/info")


class NasdaqApi(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)
        self._session = None
        self._apikey = None
        self._url = None

    @property
    def session(self):
        if self._session is None:
            self._session = BaseApi.create_session()
        return self._session

    @property
    def url(self):
        if self._url is None:
            self._url = NasdaqUrl(current_app.config.get("NASDAQ_API_URL"))
        return self._url

    def stock_info(self, symbol, params={}):
        params.update({"assetclass": "stocks"})
        resp = self.get(self.url.info(symbol), params=params)
        resp.raise_for_status()
        return resp.json()


Nasdaq = NasdaqApi()
