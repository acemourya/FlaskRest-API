from db import db
from datetime import datetime


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    user_code = db.Column(db.String(256))
    date_joined = db.Column(db.Date, default=datetime.utcnow)
