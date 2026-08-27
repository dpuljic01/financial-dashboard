from flask import current_app
import logging
import socket

from flask import render_template
from flask_mail import Message

from server.extensions import mail


log = logging.getLogger(__name__)

# flask-mail doesn't pass a timeout to smtplib, so a blocked/slow SMTP
# connection would otherwise hang on the OS default (effectively forever),
# well past gunicorn's worker timeout.
SMTP_TIMEOUT_SECONDS = 10

_original_getaddrinfo = socket.getaddrinfo


def _ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    # Render's containers have no outbound IPv6 route. smtplib tries only
    # the first address getaddrinfo returns and gives up rather than
    # falling back, and DNS for smtp.gmail.com resolves an AAAA (IPv6)
    # record first, so every send failed with "Network is unreachable".
    # Restricting to AF_INET here forces IPv4, which is actually routable.
    return _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)


def _render_email(filename, **kwargs):
    return render_template(filename, **kwargs)


def send_mail(subject, recipients, html_body):
    msg = Message(
        subject,
        recipients=recipients,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
    )
    msg.html = html_body
    previous_timeout = socket.getdefaulttimeout()
    try:
        socket.setdefaulttimeout(SMTP_TIMEOUT_SECONDS)
        socket.getaddrinfo = _ipv4_only_getaddrinfo
        mail.send(msg)
    except Exception:
        # A slow/unreachable SMTP server shouldn't take down the request
        # (or the gunicorn worker, via a timeout) that triggered this email.
        log.exception("Failed to send email: %s", subject)
    finally:
        socket.setdefaulttimeout(previous_timeout)
        socket.getaddrinfo = _original_getaddrinfo


def send_verify_email(**kwargs):
    html_message = _render_email("verify.html", **kwargs)
    send_mail("Finish your registration", [kwargs["email"]], html_message)


def send_password_reset_email(**kwargs):
    html_message = _render_email("reset.html", **kwargs)
    send_mail("Password reset", [kwargs["email"]], html_message)
