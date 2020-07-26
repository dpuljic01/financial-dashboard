from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo
)


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name",  validators=[DataRequired(), Length(max=255)])
    last_name = StringField("Last Name",  validators=[DataRequired(), Length(max=255)])
    email = StringField("Email",  validators=[Email(), Length(max=255)])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, max=255, message="Password must be at least 8 characters long")
    ])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Password",  validators=[DataRequired(), Length(max=255)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Login")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, max=255, message="Password must be at least 8 characters long")
    ])
    submit = SubmitField("Submit")


class EmailForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()])
    submit = SubmitField("Submit")


class PortfolioForm(FlaskForm):
    name = StringField("Name", validators=[Length(min=1)])
    submit = SubmitField("Submit")
