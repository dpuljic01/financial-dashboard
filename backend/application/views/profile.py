from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from application.decorators import check_confirmed
from application.models import User, Portfolio, Stock
from application.helpers.forms import PortfolioForm
from application.extensions import db


bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/")
@login_required
@check_confirmed
def get_user():
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).one_or_none()
    return render_template("profile.html", portfolio=portfolio)


@bp.route("/portfolio", methods=["GET", "POST"])
@login_required
@check_confirmed
def create_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        portfolio = Portfolio(name=form.name.data, user_id=user.id)
        user.portfolios.append(portfolio)
        db.session.add(portfolio)
        db.session.commit()
        return redirect(url_for("profile.get_user", form=form))
    user = User.query.get(current_user.id)
    return render_template("profile.html", portfolio=user.portfolios, form=form)
