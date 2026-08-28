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

    def fetch_company_overview(self, symbol):
        # Fallback for the company-info panel when yfinance's heavier
        # quoteSummary scrape comes back sparse (which it does often, since
        # that's the specific endpoint Yahoo rate-limits hardest from
        # datacenter IPs) - a completely different provider, so not subject
        # to the same block. Field names below are Alpha Vantage's OVERVIEW
        # schema; mapped to the same lowercase keys the frontend already
        # reads from the yfinance path via slugify_keys.
        data = self.fetch_data({"function": "OVERVIEW", "symbol": symbol})
        if not data or not data.get("Name"):
            return None

        def to_float(key):
            try:
                return float(data.get(key))
            except (TypeError, ValueError):
                return None

        week_low = to_float("52WeekLow")
        week_high = to_float("52WeekHigh")
        fiftytwoweekrange = f"{week_low} - {week_high}" if week_low and week_high else None

        # Alpha Vantage's DividendYield is a fraction (0.0293); yfinance's
        # dividendyield - what the frontend already renders as `${value}%` -
        # is percentage-scaled (2.93). Convert so the two sources agree.
        dividend_yield = to_float("DividendYield")
        if dividend_yield is not None:
            dividend_yield *= 100

        return {
            "symbol": data.get("Symbol"),
            "longname": data.get("Name"),
            "shortname": data.get("Name"),
            "sector": data.get("Sector"),
            "industry": data.get("Industry"),
            "longbusinesssummary": data.get("Description"),
            "website": data.get("OfficialSite"),
            "marketcap": to_float("MarketCapitalization"),
            "fulltimeemployees": to_float("FullTimeEmployees"),
            "trailingpe": to_float("PERatio"),
            "forwardpe": to_float("ForwardPE"),
            "dividendyield": dividend_yield,
            "beta": to_float("Beta"),
            "fiftytwoweekrange": fiftytwoweekrange,
        }


AlphaVantage = AlphaVantageApi()
