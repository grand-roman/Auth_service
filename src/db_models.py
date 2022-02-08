import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import TIMESTAMP
from db import db
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, Time, TIMESTAMP


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = db.Column(TIMESTAMP(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<User {self.login}>'


class LoginEvent(db.Model):
    __tablename__ = 'login_events'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete="CASCADE"))
    user = db.relationship("User")
    fingerprint = db.Column(db.JSON)
    # success = db.Column(db.Boolean)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<LoginEvent {self.login}>'
