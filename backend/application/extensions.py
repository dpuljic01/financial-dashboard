from flask_babelex import Babel
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
babel = Babel()
csrf = CSRFProtect()
