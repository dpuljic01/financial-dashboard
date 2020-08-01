from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))
    return serializer.dumps(email, salt=current_app.config.get("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=60 * 60 * 24):  # 24 hours
    serializer = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))
    try:
        email = serializer.loads(
            token,
            salt=current_app.config.get("SECURITY_PASSWORD_SALT"),
            max_age=expiration
        )
    except:
        return False
    return email
