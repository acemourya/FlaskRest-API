from db import db
from flask import request, jsonify, session, make_response
from flask.views import MethodView
from flask_smorest import Blueprint
from models.user import User
from passlib.hash import sha256_crypt

blp = Blueprint("User", __name__, description="Operations on user credential")


@blp.route("/register")
class Register(MethodView):

    def post(self):
        try:
            username = request.json['username']
            user_code = request.json['password']
            confirm_user_code = request.json['confirm_password']
            if bool(User.query.filter_by(username=username).first()) is False:
                if user_code == confirm_user_code:
                    encypt_code = sha256_crypt.encrypt(user_code)
                    entry = User(username=username, user_code=encypt_code)
                    db.session.add(entry)
                    db.session.commit()
                    user_id = User.query.filter_by(
                        username=username).first().id
                    return make_response(jsonify(id=user_id, message="Successfully register"), 200)
                return make_response(jsonify(message="Invalid username or password"), 400)
            return make_response(jsonify(message="This username already exist try another uesrname"), 400)
        except:
            return make_response(jsonify(message="Failed to register try again"), 400)


@blp.route("/login")
class Login(MethodView):

    def post(self):

        try:
            username = request.json['username']
            user_code = request.json['password']
            user = User.query.filter_by(username=username).first()
            pas = user.user_code
            if (sha256_crypt.verify(user_code, pas)):
                session['username'] = username
                return make_response(jsonify(id=user.id, message="Successfully login"), 200)
            return make_response(jsonify(message="Invalid username or password"), 400)
        except:
            return make_response(jsonify(message="Failed to login try again"), 400)
