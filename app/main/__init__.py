from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from app.main.api import api
from app.main.service.db import init_db
from .model.roles import Role
from .model.users import User
from .service.cache import jwt_redis_cache
from .utils import db_helper

db = SQLAlchemy()


def jwt_helper(jwt: JWTManager):
    """Helper function to make some validation with jwt manager."""

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_cache.get(jti)
        return token_in_redis is not None

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api.init_app(app)

    init_db()

    jwt = JWTManager(app)
    jwt_helper(jwt)

    db_helper()

    return app
