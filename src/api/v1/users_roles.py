from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from db_models import User, Role, users_roles
from db import db

# TODO: кто может назначать/удалять роли
# TODO: при добавлении/удалении роли пользователя как быть с выданными токенами

users_roles_blueprint = Blueprint("users_roles", __name__)


@users_roles_blueprint.route("/<role_id>", methods=["POST"])
@jwt_required()
def create(user_id, role_id):
    user = User.query.filter_by(id=user_id).first()
    role = Role.query.filter_by(id=role_id).first()

    user.roles.append(role)
    db.session.commit()

    return jsonify([
        {
            "id": role.id,
            "permissions": role.permissions
        } for role in user.roles
    ])


@users_roles_blueprint.route("", methods=["GET"])
@jwt_required()
def read(user_id):
    user = User.query.filter_by(id=user_id).first()

    return jsonify([
        {
            "id": role.id,
            "permissions": role.permissions
        } for role in user.roles
    ])


@users_roles_blueprint.route("/<role_id>", methods=["DELETE"])
@jwt_required()
def delete(user_id, role_id):
    user = User.query.filter_by(id=user_id).first()
    role = Role.query.filter_by(id=role_id).first()

    user.roles.remove(role)
    db.session.commit()

    return jsonify({'success': True})
