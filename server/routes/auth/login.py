from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from config import db
from models.user import User
from schemas.user_schema import UserSchema

user_schema = UserSchema(session=db.session)


class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = User.query.filter_by(email=data.get("email")).first()

            if user and user.authenticate(data.get("password")):
                jwt = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                serialized_user = user_schema.dump(user)
                response = make_response(serialized_user, 200)
                set_access_cookies(response, jwt)
                set_refresh_cookies(response, refresh_token)
                return response

            return {"message": "Invalid User Credentials"}, 403

        except Exception as e:
            return {"message": str(e)}, 403
