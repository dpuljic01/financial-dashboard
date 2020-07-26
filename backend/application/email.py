from flask import current_app
from flask import render_template, url_for
from flask_mail import Message

from application.extensions import mail


def send_email(html, redirect, recipients, subject, token):
    url = url_for(redirect, token=token, _external=True)
    template = render_template(html, url=url)
    msg = Message(
        subject=subject,
        recipients=[recipients],
        html=template,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )
    mail.send(msg)
