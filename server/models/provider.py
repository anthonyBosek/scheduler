from sqlalchemy import validates
from sqlalchemy.ext.hybrid import hybrid_pproperty
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, Bcrypt

class Provider(db.Model):
    __tablename__ = "providers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#! relationships

#! validations
    


