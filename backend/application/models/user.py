from uuid import uuid4

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import PasswordType

from application.extensions import db
from application.extensions import login
from application.models.mixin import TimestampMixin


@login.user_loader
def load_user(uuid):
    return User.query.get(uuid)


def get_uuid():
    return str(uuid4())


class User(UserMixin, db.Model, TimestampMixin):
    """
    User model.
    `account_type`: `basic` and `premium`, also `admin`, but not sure about that yet. It"s `basic` by default
    `status`: by default inactive, becomes active after email confirmation
    """
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password = db.Column(PasswordType(schemes=["bcrypt"]), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, server_default="1")
    confirmed = db.Column(db.Boolean(), nullable=False, server_default="0")
    email_confirmed_at = db.Column(db.DateTime())

    portfolios = db.relationship("Portfolio", back_populates="user")
    roles = db.relationship("Role", secondary="user_roles")

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @staticmethod
    def auth(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return user
        return None

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
