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
    CACHE_TYPE = "simple"  # Flask-Caching related configs
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

    MONGO_DB_CONNECTION_STRING = os.getenv("MONGO_DB_CONNECTION_STRING")
    PROXIES = os.getenv("PROXIES", None)


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    FLASK_ENV = "development"


class TestingConfig(Config):
    TESTING = True
