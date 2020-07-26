from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, abort, jsonify, make_response
from flask_login import login_user, logout_user, current_user, login_required
from marshmallow import fields
from marshmallow import validate
from validate_email import validate_email
from webargs.flaskparser import use_kwargs


from application.extensions import db
from application.email import send_email
from application.helpers.errors import flash_errors
from application.helpers.forms import RegistrationForm, LoginForm, ResetPasswordForm, EmailForm
from application.models import User
from application.token import generate_confirmation_token, confirm_token

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
@use_kwargs({
    "email": fields.String(required=True, validate=validate.Email()),
    "password": fields.String(required=True, validate=validate.Length(min=1, max=255)),
    "remember": fields.Boolean(missing=False)
})
def login(**payload):
    db_user = User.auth(email=payload["email"], password=payload["password"])

    if not db_user:
        return make_response(jsonify(error_code="INVALID_LOGIN", message="Login failed.")), 400

    if not db_user.confirmed:
        return make_response(jsonify(error_code="INVALID_LOGIN", message="User is not verified.")), 400

    login_user(user=db_user, remember=payload["remember"])
    return "", 204


@bp.route("/register", methods=["POST"])
@use_kwargs({
    "first_name": fields.String(required=True, validate=validate.Length(min=1, max=255)),
    "last_name": fields.String(required=True, validate=validate.Length(min=1, max=255)),
    "email": fields.String(required=True, validate=validate.Email()),
    "password": fields.String(required=True, validate=validate.Length(min=8, max=255))
})
def register(**payload):
    db_user = User.query.filter_by(email=payload["email"]).first()
    if db_user:
        return make_response(jsonify(error_code="INVALID_LOGIN", message="Email already exists.")), 409

    db_user = User(
        first_name=payload["first_name"],
        last_name=payload["last_name"],
        email=payload["email"],
        password=payload["password"]
    )

    # add the new user to the database
    db.session.add(db_user)
    db.session.commit()

    token = generate_confirmation_token(db_user.email)
    send_email(
        redirect="auth.confirm_email",
        html="activate.html",
        recipients=db_user.email,
        subject="Please confirm your email",
        token=token
    )

    login_user(db_user)  # hmmmmmmmmmm
    return "", 204


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return "", 204


@bp.route("/confirm/<string:token>")
@login_required
def confirm_email(token):
    email = confirm_token(token)

    if not email:
        return make_response(jsonify(error_code="INVALID_ARGUMENT", message="The confirmation link is invalid or has expired.")), 400

    db_user = User.query.filter_by(email=email).first_or_404()
    db_user.confirmed = True
    db_user.email_confirmed_at = datetime.utcnow()
    db.session.commit()

    return "", 204


@bp.route("/unconfirmed", methods=["GET"])
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("main.profile"))
    flash("Please confirm your account!")
    return render_template("unconfirmed.html")


@bp.route("/resend")
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    send_email(
        redirect="auth.confirm_email",
        html="activate.html",
        recipients=current_user.email,
        subject="Please confirm your email",
        token=token
    )
    flash("A new confirmation email has been sent.")
    return redirect(url_for("auth.unconfirmed"))


@bp.route("/reset", methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        token = generate_confirmation_token(user.email)
        send_email(
            redirect="auth.reset_with_token",
            html="recover.html",
            recipients=user.email,
            subject="Password reset requested",
            token=token
        )
        flash("Check your email.")
        return redirect(url_for("auth.login"))
    return render_template("login.html")


@bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_with_token(token):
    email = confirm_token(token)
    if not email:
        flash("The confirmation link is invalid or has expired.")
        return render_template("login.html")

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("reset_with_token.html", form=form, token=token)
