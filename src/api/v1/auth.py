from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from db import db
from no_sql_db import redis_db
from db_models import User, LoginEvent

auth_blueprint = Blueprint("auth", __name__, url_prefix="auth")


class ParamsException(Exception):
    pass


@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        login = request.json['login']
        password = request.json['password']
    except ParamsException:
        return {"error": ""}

    # TODO: hash password
    password_hash = password

    user = User.query.filter_by(login=login, password=password_hash).first()
    if not user:
        return {"error": "user not found"}

    # TODO: EXPIRE
    access_token = create_access_token(identity=user.login)
    refresh_token = create_refresh_token(identity=user.login)

    # TODO: backoff?
    redis_db.set('{}:{}'.format(user.login, 'refresh_token'), refresh_token)

    login_event = LoginEvent(
        user=user,
        fingerprint=dict()
    )
    db.session.add(login_event)
    db.session.commit()

    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    login = get_jwt_identity()
    token = redis_db.get('{}:{}'.format(login, 'refresh_token'))
    if not token or token.decode() != request.headers.get("Authorization").split()[1]:
        return {"error": ""}

    access_token = create_access_token(identity=login)
    refresh_token = create_refresh_token(identity=login)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    login = get_jwt_identity()
    redis_db.delete('{}:{}'.format(login, 'refresh_token'))
    return jsonify({"success": True})


@auth_blueprint.route("/history", methods=["GET"])
@jwt_required()
def history():
    login = get_jwt_identity()

    user = User.query.filter_by(login=login).first()
    login_events = LoginEvent.query.filter_by(user_id=user.id)

    result = [
        {
            "id": event.id,
            "user": event.user_id,
            "created_at": event.created_at,
        } for event in login_events.all()
    ]

    return jsonify(result)
