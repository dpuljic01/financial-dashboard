from urllib.parse import urljoin
from flask import current_app
import requests


class AlphaVantageUrl:
    def __init__(self, root):
        self.root = root

    def make(self, *args):
        return urljoin(self.root, *args)

    def query(self):
        return self.make("/query")


class AlphaVantageApi:
    def __init__(self):
        self._apikey = None
        self._url = None

    def get(self, url, **kwargs):  # probably move all these into separate file and inherit from it
        return requests.get(url, **kwargs)

    def post(self, url, **kwargs):
        return requests.post(url, **kwargs)

    def put(self, url, **kwargs):
        return requests.put(url, **kwargs)

    def delete(self, url, **kwargs):
        return requests.delete(url, **kwargs)  

    @property
    def apikey(self):
        if self._apikey is None:
            self._apikey = current_app.config.get("ALPHA_VANTAGE_API_KEY")
        return self._apikey
    
    @property
    def url(self):
        if self._url is None:
            self._url = AlphaVantageUrl(current_app.config.get("ALPHA_VANTAGE_API_URL"))
        return self._url

    def fetch_data(self, params):
        params.update({"apikey": self.apikey})
        resp = requests.get(self.url.query(), params=params)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def filter_global_quote(data):
        quote = data["Global Quote"]
        return {k.split(" ")[1]: v for k, v in quote.items()}


AlphaVantage = AlphaVantageApi()
