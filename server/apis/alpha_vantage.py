from urllib.parse import urljoin
from flask import current_app
from server.apis.base_api import BaseApi


class AlphaVantageUrl:
    def __init__(self, root):
        self.root = root

    def make(self, *args):
        return urljoin(self.root, *args)

    def query(self):
        return self.make("/query")


class AlphaVantageApi(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)
        self._session = None
        self._apikey = None
        self._url = None

    @property
    def apikey(self):
        if self._apikey is None:
            self._apikey = current_app.config.get("ALPHA_VANTAGE_API_KEY")
        return self._apikey

    @property
    def session(self):
        if self._session is None:
            self._session = BaseApi.create_session()
            self._session.params.update({"apikey": self.apikey})
        return self._session

    @property
    def url(self):
        if self._url is None:
            self._url = AlphaVantageUrl(current_app.config.get("ALPHA_VANTAGE_API_URL"))
        return self._url

    def fetch_data(self, params):
        resp = self.get(self.url.query(), params=params)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def filter_global_quote(data):
        quote = data["Global Quote"]
        return {k.split(" ")[1]: v for k, v in quote.items()}


AlphaVantage = AlphaVantageApi()
