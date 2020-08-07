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

    FINANCIAL_DASHBOARD_FE_URL = os.getenv("FINANCIAL_DASHBOARD_FE_URL", "http://127.0.0.1:8080")
    # limit for free keys: (5 API requests per minute; 500 API requests per day)
    ALPHA_VANTAGE_API_URL = os.getenv("ALPHA_VANTAGE_API_URL", "https://www.alphavantage.co")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

    # limit for free: (50.000 API requests per day, but no concurrent calls) - not the newest data :(
    # QUANDL_API_URL = os.getenv("QUANDL_API_URL", "https://www.quandl.com/")
    # QUANDL_API_KEY = os.getenv("QUANDL_API_KEY")

    # unlimited mocked data, 50k messages/mo on production (free plan)
    IEX_BASE_URL = os.getenv("IEX_BASE_URL", "https://sandbox.iexapis.com/")  # prod https://cloud.iexapis.com/v1/
    IEX_TOKEN = os.getenv("IEX_TOKEN")

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Financial Dashboard", "financial.dashboard.info@gmail.com")

    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")

    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 60 * 60 * 24 * 30))
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, "dist")

    if not os.path.exists(DIST_DIR):
        raise Exception("DIST_DIR not found: {}".format(DIST_DIR))

    SHOULD_PROXY = bool(int(os.getenv("SHOULD_PROXY", "1")))


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    FLASK_ENV = "development"
    # MAIL_SUPPRESS_SEND = True


class TestingConfig(Config):
    TESTING = True
