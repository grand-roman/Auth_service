from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from db_models import Role
from db import db

role_blueprint = Blueprint("role", __name__, url_prefix="role")


# TODO: кто может удалять, создавать, изменять роли


@role_blueprint.route("", methods=["POST"])
@jwt_required()
def create():
    try:
        name: str = request.json['name']
        permissions: list = request.json['permissions']
    except KeyError:
        return None

    role = Role(
        name=name,
        permissions=permissions
    )
    db.session.add(role)
    db.session.commit()

    return jsonify({
        "id": role.id,
        "name": role.name,
        "permissions": role.permissions
    })


@role_blueprint.route("/<role_id>", methods=["GET"])
@jwt_required()
def read(role_id):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return jsonify()

    return jsonify({
        "id": role.id,
        "name": role.name,
        "permissions": role.permissions
    })


@role_blueprint.route("/<role_id>", methods=["PUT"])
@jwt_required()
def update(role_id):
    try:
        name: str = request.json['name']
        permissions: list = request.json['permissions']
    except KeyError:
        return None

    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return None

    role.name = name
    role.permissions = permissions

    db.session.add(role)
    db.session.commit()

    return jsonify({
        "id": role.id,
        "name": role.name,
        "permissions": role.permissions
    })


@role_blueprint.route("/<role_id>", methods=["DELETE"])
@jwt_required()
def delete(role_id):
    role = Role.query.filter_by(id=role_id)
    if not role:
        return None

    role.delete()
    db.session.commit()

    return jsonify({"success": True})
