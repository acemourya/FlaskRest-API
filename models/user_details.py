from db import db


class UserDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=False, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(800), nullable=True)
