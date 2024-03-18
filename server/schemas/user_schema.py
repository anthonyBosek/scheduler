from marshmallow import fields, validate
from config import ma
from models.user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        fields = [
            "id",
            "first_name",
            "last_name",
            "location",
            "username",
            "email",
        ]

    first_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    location = fields.String(required=True, validate=validate.Length(min=2, max=80))
    username = fields.String(required=True, validate=validate.Length(min=2, max=50))
    email = fields.String(required=True, validate=validate.Length(min=2, max=256))
