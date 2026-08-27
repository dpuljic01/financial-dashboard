import logging

import requests
from flask import current_app, render_template

log = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"
REQUEST_TIMEOUT_SECONDS = 10


def _render_email(filename, **kwargs):
    return render_template(filename, **kwargs)


def send_mail(subject, recipients, html_body, text_body):
    api_key = current_app.config.get("RESEND_API_KEY")
    if not api_key:
        log.warning("RESEND_API_KEY not set, skipping email: %s", subject)
        return

    try:
        response = requests.post(
            RESEND_API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "from": current_app.config.get("RESEND_FROM"),
                "to": recipients,
                "subject": subject,
                "html": html_body,
                "text": text_body,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except Exception:
        # A failing email provider shouldn't take down the request that
        # triggered it (registration, password reset, ...).
        log.exception("Failed to send email: %s", subject)


def send_verify_email(**kwargs):
    html_message = _render_email("verify.html", **kwargs)
    text_message = _render_email("verify.txt", **kwargs)
    send_mail("Finish your registration", [kwargs["email"]], html_message, text_message)


def send_password_reset_email(**kwargs):
    html_message = _render_email("reset.html", **kwargs)
    text_message = _render_email("reset.txt", **kwargs)
    send_mail("Password reset", [kwargs["email"]], html_message, text_message)
