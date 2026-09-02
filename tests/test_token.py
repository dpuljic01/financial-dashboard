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
        # The token itself is opaque (a random string, not the email encoded
        # into it) - confirm_token is the only way to recover the email.
        assert 'user@example.com' not in token
        assert confirm_token(token) == 'user@example.com'
        # Single-use: the same link can't be replayed after it's been consumed.
        assert confirm_token(token) is False


def test_token_unknown_is_rejected(monkeypatch):
    monkeypatch.setenv('APP_SETTINGS', 'server.config.TestingConfig')
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///:memory:')
    app = create_app()
    app.config['SECRET_KEY'] = 'testing-secret'
    app.config['SECURITY_PASSWORD_SALT'] = 'salty'
    with app.app_context():
        assert confirm_token('not-a-real-token') is False


