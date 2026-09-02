import secrets

from server.common.cache import Cache

TOKEN_TTL = 60 * 60 * 24  # 24 hours
TOKEN_KEY_PREFIX = "confirm-token:"


def generate_confirmation_token(email):
    # A short opaque token looked up server-side, rather than the previous
    # itsdangerous-signed token - that packed the recipient's email address
    # (base64, trivially decodable) directly into the emailed link, which
    # both leaks the address to anyone who intercepts or forwards it and is
    # a well-known phishing-kit shape (pre-filling a credential-harvesting
    # page with the victim's email) that spam/content classifiers are
    # trained to flag, independent of sender reputation.
    token = secrets.token_urlsafe(32)
    Cache().set(TOKEN_KEY_PREFIX + token, email, ttl=TOKEN_TTL)
    return token


def confirm_token(token):
    found, email = Cache().get(TOKEN_KEY_PREFIX + token)
    if not found:
        return False
    # Single-use: burn it on first successful lookup so the same emailed
    # link can't be replayed after a confirm/reset has already gone through.
    Cache().delete(TOKEN_KEY_PREFIX + token)
    return email
