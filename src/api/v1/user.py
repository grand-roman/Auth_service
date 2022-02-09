from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db_models import User
from db import db
from utils.password import hash_password

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/", methods=["POST"])
def create():
    try:
        login: str = request.json['login']
        password: str = request.json['password']
    except KeyError:
        return None

    user = User(
        login=login,
        password=hash_password(password)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "login": user.login,
    })


@user_blueprint.route("/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    try:
        login: str = get_jwt_identity()
        password: str = request.json['password']
        new_password: str = request.json['new_password']
    except KeyError:
        return None

    user = User.query.filter_by(
        login=login,
        password=hash_password(password)
    ).first()
    if not user:
        return None

    user.password = hash_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "login": user.login,
    })
