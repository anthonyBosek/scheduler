from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    current_user,
)
from config import db
from schemas.user_schema import UserSchema

user_schema = UserSchema(session=db.session)


class Me(Resource):
    @jwt_required()
    def get(self):
        return user_schema.dump(current_user), 200
