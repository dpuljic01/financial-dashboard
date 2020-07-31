from flask import current_app
import logging

from flask import render_template
from flask_mail import Message

from application.extensions import mail


log = logging.getLogger(__name__)


def _render_email(filename, **kwargs):
    return render_template(filename, **kwargs)


def send_mail(subject, recipients, html_body):
    msg = Message(
        subject,
        recipients=recipients,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )
    msg.html = html_body
    mail.send(msg)


def send_verify_email(**kwargs):
    html_message = _render_email("verify.html", **kwargs)
    send_mail("Finish your registration", [kwargs["email"]], html_message)


def send_password_reset_email(**kwargs):
    html_message = _render_email("reset.html", **kwargs)
    send_mail("Password reset", [kwargs["email"]], html_message)


# def send_email(html, redirect, recipients, subject, token):
#     url = url_for(redirect, token=token, _external=True)
#     template = render_template(html, url=url)
#     msg = Message(
#         subject=subject,
#         recipients=[recipients],
#         html=template,
#         sender=current_app.config.get("MAIL_DEFAULT_SENDER")
#     )
#     mail.send(msg)
