from db import db
from flask import request, jsonify, session
from flask.views import MethodView
from flask_smorest import Blueprint
from models.user import User
from passlib.hash import sha256_crypt

blp = Blueprint("User", __name__, description="Operations on user credential")


@blp.route("/register")
class Register(MethodView):

    def post(self):
        try:
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if bool(User.query.filter_by(username=username).first()) is False:
                if password == confirm_password:
                    encyptpass = sha256_crypt.encrypt(password)
                    entry = User(username=username, password=encyptpass)
                    db.create_all()
                    db.session.add(entry)
                    db.session.commit()
                    return jsonify({"status": 200, "message": "Successfully register"})
                return jsonify({"status": 400, "message": "Invalid username or password"})
            return jsonify({"status": 400, "message": "This username already exist try another"})
        except:
            return jsonify({"status": 400, "message": "Failed to register try again"})


@blp.route("/login")
class Login(MethodView):

    def post(self):

        try:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            pas = user.password
            if (sha256_crypt.verify(password, pas)):
                print(user)
                session['username'] = username
                print(user, pas)
                return jsonify({"status": 200, "message": "Success login"})
            return jsonify({"status": 400, "message": "Invalid username or password"})
        except:
            return jsonify({"status": 400, "message": "Failed to login try again"})
