from flask import Blueprint

auth_blueprint = Blueprint("role", __name__)


@auth_blueprint.route("/", methods=["POST"])
def create():
    pass


@auth_blueprint.route("/{user_id}", methods=["PUT"])
def update():
    pass


@auth_blueprint.route("/{user_id}", methods=["DELETE"])
def update():
    pass
