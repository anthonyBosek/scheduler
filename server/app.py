#! /usr/bin/env python3

from config import app, db, api, jwt
from werkzeug.exceptions import NotFound

# models
from models.user import User


# auth routes
from routes.auth.login import Login
from routes.auth.logout import Logout
from routes.auth.me import Me
from routes.auth.refresh import Refresh
from routes.auth.register import Register

# routes


# api auth resources
api.add_resource(Login, "/auth/login")
api.add_resource(Logout, "/auth/logout")
api.add_resource(Me, "/auth/me")
api.add_resource(Refresh, "/auth/refresh")
api.add_resource(Register, "/auth/register")

# api resources


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.session.get(User, identity)


@app.errorhandler(NotFound)
def handle_404(error):
    response = {"message": error.description}
    return response, error.code


@app.route("/")
def index():
    return "Scheduler API"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
