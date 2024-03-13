from flask_restful import Resource
from flask import make_response
from flask_jwt_extended import (
    jwt_required,
    current_user,
    create_access_token,
    set_access_cookies,
    get_jwt_identity,
)
from config import db
from schemas.user_schema import UserSchema

user_schema = UserSchema(session=db.session)


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        id_ = get_jwt_identity()
        res = make_response(user_schema.dump(current_user), 200)
        access_token = create_access_token(identity=id_)
        set_access_cookies(res, access_token)
        return res
