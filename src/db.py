from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@postgres/auth'
    from db_models import User
    db.init_app(app)
    app.app_context().push()
    db.create_all()
