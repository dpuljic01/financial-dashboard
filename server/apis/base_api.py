from flask import current_app
from requests.adapters import HTTPAdapter
from requests.sessions import Session


class BaseApi:
    def __getattr__(self, name):
        if name not in ("get", "post", "put", "delete"):
            raise AttributeError

        fname = f"_{name}"
        fn = getattr(self, fname)

        return fn

    def _get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def _post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    def _put(self, url, **kwargs):
        return self.session.put(url, **kwargs)

    def _delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)

    @staticmethod
    def create_session():
        adapter = HTTPAdapter(max_retries=3)
        session = Session()

        default_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        user_agent = current_app.config.get("USER_AGENT", default_ua)
        session.headers["User-Agent"] = user_agent
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
