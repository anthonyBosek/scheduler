from sqlalchemy.orm import validates
import re
from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from models.mixins import TimestampMixin


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    @validates("first_name")
    def validate_first_name(self, _, first_name):
        if not first_name:
            raise AssertionError("First name is required")
        if len(first_name) < 2:
            raise ValueError("First name must be at least 2 characters")
        if len(first_name) > 50:
            raise ValueError("First name must be less than 50 characters")
        return first_name

    @validates("last_name")
    def validate_last_name(self, _, last_name):
        if not last_name:
            raise AssertionError("Last name is required")
        elif len(last_name) < 2:
            raise ValueError("Last name must be at least 2 characters")
        elif len(last_name) > 50:
            raise ValueError("Last name must be less than 50 characters")
        return last_name

    @validates("location")
    def validate_location(self, _, location):
        if not location:
            raise AssertionError("Location is required")
        elif len(location) < 2:
            raise ValueError("Location must be at least 2 characters")
        elif len(location) > 80:
            raise ValueError("Location must be less than 80 characters")
        return location

    @validates("username")
    def validate_username(self, _, new_username):
        if not new_username:
            raise AssertionError("Username is required")
        elif len(new_username) < 2:
            raise ValueError("Username must be at least 2 characters")
        elif len(new_username) > 50:
            raise ValueError("Username must be less than 50 characters")
        elif db.session.query(User).filter_by(username=new_username).first():
            raise ValueError("Username is already taken")
        return new_username

    @validates("email")
    def validate_email(self, _, email_):
        if not email_:
            raise AssertionError("Email is required")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email_):
            raise ValueError("Email must be valid")
        elif db.session.query(User).filter_by(email=email_).first():
            raise ValueError("Email is already taken")
        return email_

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash is not readable")

    @password_hash.setter
    def password_hash(self, new_password):
        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        self._password_hash = hashed_password

    def authenticate(self, password_to_check):
        return bcrypt.check_password_hash(self._password_hash, password_to_check)

    def __repr__(self):
        return f"<User #{self.id} {self.username} />"
