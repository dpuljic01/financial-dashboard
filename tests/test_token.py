import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import create_app
from server.token import generate_confirmation_token, confirm_token


def test_token_round_trip(monkeypatch):
    monkeypatch.setenv('APP_SETTINGS', 'server.config.TestingConfig')
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///:memory:')
    app = create_app()
    app.config['SECRET_KEY'] = 'testing-secret'
    app.config['SECURITY_PASSWORD_SALT'] = 'salty'
    with app.app_context():
        token = generate_confirmation_token('user@example.com')
        assert confirm_token(token) == 'user@example.com'


