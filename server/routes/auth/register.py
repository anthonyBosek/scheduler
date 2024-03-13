from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from sqlalchemy.exc import IntegrityError
from config import db
from schemas.user_schema import UserSchema

user_schema = UserSchema(session=db.session)


class Register(Resource):
    def post(self):
        print(request.get_json())
        try:
            data = {
                "first_name": request.get_json().get("first_name"),
                "last_name": request.get_json().get("last_name"),
                "location": request.get_json().get("location"),
                "favorite_team": request.get_json().get("favorite_team"),
                "username": request.get_json().get("username"),
                "email": request.get_json().get("email"),
            }
            user_schema.validate(data)
            user = user_schema.load(data)
            user.password_hash = request.get_json().get("password")
            db.session.add(user)
            db.session.commit()
            jwt = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            serialized_user = user_schema.dump(user)
            response = make_response({"user": serialized_user}, 201)
            set_access_cookies(response, jwt)
            set_refresh_cookies(response, refresh_token)
            return response

        except (Exception, IntegrityError) as e:
            db.session.rollback()
            return {"message": str(e)}, 400
