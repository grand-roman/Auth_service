import os

import redis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
redis_db = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT", 6379), db=0)
