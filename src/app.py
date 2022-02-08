import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from db import init_db

from api.v1.auth import auth_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix="/api/v1")

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)


def main():
    init_db(app)
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))


if __name__ == '__main__':
    main()
