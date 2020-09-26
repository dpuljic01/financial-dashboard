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

    def news(self, symbol):
        return self.make(
            f"/api/v1/news-headlines-fetcher/{symbol.upper()}/0/4"
        )  # first four

    def movers(self):
        return self.make("/api/marketmovers")


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

    def get_headlines(self, symbol):
        url = self.url.news(symbol).replace("api", "www", 1)
        resp = self.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                "Referer": f"https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}/press-releases",
            },
        )
        resp.raise_for_status()
        return resp

    def get_market_movers(self, params={}):
        params.update(
            {"assetclass": "STOCKS", "exchangestatus": "currentMarket", "limit": 5}
        )
        resp = self.get(self.url.movers(), params=params)
        resp.raise_for_status()
        return resp.json()


Nasdaq = NasdaqApi()
