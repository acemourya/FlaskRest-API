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
            user_code = request.form['password']
            confirm_user_code = request.form['confirm_password']
            if bool(User.query.filter_by(username=username).first()) is False:
                if user_code == confirm_user_code:
                    encypt_code = sha256_crypt.encrypt(user_code)
                    entry = User(username=username, user_code=encypt_code)
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
            user_code = request.form['password']
            user = User.query.filter_by(username=username).first()
            pas = user.user_code
            if (sha256_crypt.verify(user_code, pas)):
                session['username'] = username
                return jsonify({"status": 200, "message": "Successfully login"})
            return jsonify({"status": 400, "message": "Invalid username or password"})
        except:
            return jsonify({"status": 400, "message": "Failed to login try again"})
