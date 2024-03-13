from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = os.environ.get("APP_SECRET")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
#! In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
#! Change time in production
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
#! Change time in production
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
#! Restricts JWT to https protocols only
#! app.config["JWT_COOKIE_CSRF_PROTECT"] = True
#! app.config["PROPAGATE_EXCEPTIONS"] = True
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
