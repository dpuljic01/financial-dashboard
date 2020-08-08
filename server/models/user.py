from uuid import uuid4
import os
import binascii
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import PasswordType


from server.extensions import db
from server.models.mixin import TimestampMixin


def get_uuid():
    return str(uuid4())


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password = db.Column(PasswordType(schemes=["bcrypt"]))
    is_active = db.Column(db.Boolean(), nullable=False, server_default="1")
    confirmed = db.Column(db.Boolean(), nullable=False, server_default="0")
    email_confirmed_at = db.Column(db.DateTime())
    last_logged_in = db.Column(db.DateTime())

    portfolios = db.relationship("Portfolio", back_populates="user")
    roles = db.relationship("Role", secondary="user_roles")

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if not self.password:
            self.password = binascii.hexlify(os.urandom(24)).decode()

    @classmethod
    def auth(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or user.password != password:
            return None

        return user

    @property
    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "portfolios": [portfolio.json for portfolio in self.portfolios],
        }

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, first_name={self.first_name}, " \
               f"last_name={self.last_name}), confirmed={self.confirmed}"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
