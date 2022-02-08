from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db_models import User
from db import db

user_blueprint = Blueprint("user", __name__)


# TODO: hash password

@user_blueprint.route("/", methods=["POST"])
def create():
    try:
        login: str = request.json['login']
        password: list = request.json['password']
    except KeyError:
        return None

    user = User(
        login=login,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "login": user.login,
    })


@user_blueprint.route("", methods=["PUT"])
@jwt_required()
def update():
    try:
        login: str = get_jwt_identity()
        password: list = request.json['password']
    except KeyError:
        return None

    user = User.query.filter_by(login=login, password=password).first()
    if not user:
        return None

    user.password = password
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "login": user.login,
    })
