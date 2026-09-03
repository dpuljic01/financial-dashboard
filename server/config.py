import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    FLASK_APP = "wsgi.py"
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "Fallback Secret Key")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Neon suspends its compute after a few idle minutes. Without pool_pre_ping,
    # the pool's first checkout after a suspend hands out a connection that's
    # already dead, and the query fails with a 500 - refreshing "fixes" it only
    # because the retry gets a fresh connection. pre_ping tests each connection
    # with a cheap SELECT 1 before use and transparently reopens it if it's
    # gone, so this happens invisibly instead of surfacing as an error.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    # Was "simple" (an in-process dict) - with gunicorn running multiple
    # workers, each worker had its own private cache, so a cached response
    # from worker A was invisible to worker B, and any restart (including
    # the free-tier spin-down/wake-up cycle) wiped it entirely. That badly
    # undercut the company-info cache meant to protect Alpha Vantage's
    # 25-requests/day quota. Redis is already provisioned and used
    # elsewhere (JWT blacklist) - point the cache at it too for one shared,
    # restart-surviving cache.
    CACHE_TYPE = "RedisCache"  # Flask-Caching related configs
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
    CACHE_DEFAULT_TIMEOUT = 300  # 5min

    FINANCIAL_DASHBOARD_FE_URL = os.getenv(
        "FINANCIAL_DASHBOARD_FE_URL", "http://127.0.0.1:8080"
    )
    # limit for free keys: (5 API requests per minute; 500 API requests per day)
    ALPHA_VANTAGE_API_URL = os.getenv(
        "ALPHA_VANTAGE_API_URL", "https://www.alphavantage.co"
    )
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    NASDAQ_API_URL = os.getenv("NASDAQ_API_URL", "https://api.nasdaq.com")

    # unlimited mocked data, 50k messages/mo on production (free plan)
    IEX_BASE_URL = os.getenv(
        "IEX_BASE_URL", "https://sandbox.iexapis.com/"
    )  # prod https://cloud.iexapis.com/
    IEX_TOKEN = os.getenv("IEX_TOKEN")

    # Resend (https://resend.com) sends over HTTPS - unlike raw SMTP, this
    # isn't subject to hosting providers blocking outbound SMTP ports.
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    RESEND_FROM = os.getenv("RESEND_FROM", "Financial Dashboard <onboarding@resend.dev>")

    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")

    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 60 * 60 * 24 * 30)
    )
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, "dist")
    SHOULD_PROXY = bool(int(os.getenv("SHOULD_PROXY", "0")))
    if not os.path.exists(DIST_DIR) and SHOULD_PROXY:
        raise Exception(
            "DIST_DIR not found: {}. You should run `npm run build` first".format(
                DIST_DIR
            )
        )

    PROXIES = os.getenv("PROXIES", None)


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    FLASK_ENV = "development"


class TestingConfig(Config):
    TESTING = True
