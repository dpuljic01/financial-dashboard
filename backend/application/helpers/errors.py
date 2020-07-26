from flask import flash


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            data = getattr(form, field).label.text
            flash(f"{data} - {error}")


class BaseAppError(Exception):
    def __init__(self, message, error_code, status_code):
        super().__init__()
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

    def __str__(self):
        return self.message


class UniqueConstraintError(BaseAppError):
    def __init__(self, message):
        super().__init__(
            message,
            'UNIQUE_CHECK_FAILED',
            409
        )


class ExternalApiError(BaseAppError):
    def __init__(self, message, status=500):
        super().__init__(
            message,
            'EXTERNAL_API_ERROR',
            status
        )


class PermissionDeniedError(BaseAppError):
    def __init__(self, message):
        super().__init__(
            message,
            'PERMISSION_CHECK_FAILED',
            403
        )


class IdentityError(BaseAppError):
    def __init__(self):
        super().__init__(
            "Missing or invalid authorization headers",
            "INVALID_ARGUMENT",
            401
        )


class InvalidValueError(BaseAppError):
    def __init__(self, message):
        super().__init__(
            message,
            'INVALID_ARGUMENT',
            400
        )


class BadRequestError(BaseAppError):
    def __init__(self, message, error_code=400, status_code=400):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code
        )


class NotFoundError(BaseAppError):
    def __init__(self, message):
        super().__init__(
            message,
            'NOT_FOUND',
            404
        )
