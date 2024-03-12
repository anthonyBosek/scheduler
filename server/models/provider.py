from sqlalchemy import validates
from sqlalchemy.ext.hybrid import hybrid_pproperty
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt
import re

class Provider(db.Model):
    __tablename__ = "providers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#! relationships

#! validations
    
@validates("first_name")
def validate_first(self, _, first):
    if not isinstance(first, str):
        raise TypeError("First name must be a string")
    elif len(first) < 1 or len(first) > 50:
        raise ValueError("First name must be between 1-50 characters")
    return first.title()

@validates("last_name")
def validate_last(self, _, last):
    if not isinstance(last, str):
        raise TypeError("Last name must be a string")
    elif len(last) < 1 or len(last) > 50:
        raise ValueError("Last name must be between 1-50 characters")
    return last.title()

@validates("title")
def validate_title(self, _, title):
    if not isinstance(title, str):
        raise TypeError("Title must be a string")
    elif len(title) < 5 or len(title) > 50:
        raise ValueError("Title must be between 5-50 characters")
    return title.lower()

@validates("email")
def validate_email(self, _, email):
    if not isinstance(email, str):
        raise TypeError("Email must be a string")
    elif not re.match(r"/^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/"):
        raise ValueError("Email must be valid")
    return email.lower()

@validates("phone")
def validate_phone(self, _, phone):
    if not re.match(r"^\(\d{10})$"):
        raise ValueError("Phone number must be in valid format")
    return phone


