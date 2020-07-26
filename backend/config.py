import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    FLASK_APP = "wsgi.py"
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # limit for free keys: (5 API requests per minute; 500 API requests per day)
    ALPHA_VANTAGE_API_URL = os.getenv("ALPHA_VANTAGE_API_URL", "https://www.alphavantage.co")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    # limit for free: (50.000 API requests per day, but no concurrent calls)
    QUANDL_API_URL = os.getenv("QUANDL_API_URL", "https://www.quandl.com")
    QUANDL_API_KEY = os.getenv("QUANDL_API_KEY")

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Financial Dashboard", "financial.dashboard.info@gmail.com")

    # Flask-User settings
    # USER_APP_NAME = "Financial Dashboard"       # Shown in an email templates and page footers
    # USER_ENABLE_EMAIL = True                    # Enable email authentication
    # USER_ENABLE_USERNAME = False                 # Enable username authentication
    # USER_EMAIL_SENDER_NAME = USER_APP_NAME
    # USER_EMAIL_SENDER_EMAIL = MAIL_USERNAME


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    FLASK_ENV = "development"
    # MAIL_SUPPRESS_SEND = True


class TestingConfig(Config):
    TESTING = True
