import jwt

from functools import wraps

from flask import request, current_app, jsonify
from flask_jwt_extended import get_jwt_identity

from server.models import User


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_identity = get_jwt_identity()
        db_user = User.query.get(current_identity)
        if not db_user.confirmed:
            return jsonify({"message": "User not verified.", "authenticated": False, "confirmed": False}), 403
        return func(*args, **kwargs)
    return decorated_function


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()

        invalid_msg = {
            "message": "Invalid token. Authentication required.",
            "authenticated": False
        }
        expired_msg = {
            "message": "Expired token. Re-authentication required.",
            "authenticated": False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config["SECRET_KEY"])
            user = User.query.filter_by(email=data["sub"]).first()
            if not user:
                raise RuntimeError("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify
