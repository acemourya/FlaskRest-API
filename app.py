import models
from db import db
from flask import Flask
from flask_smorest import Api
from resources.user import blp as UserBlueprint
from resources.user_details import blp as UserDetailsBlueprint


def create_app():

    app = Flask(__name__)
    app.secret_key = 'super_secret-key'

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "User Rest API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPEN_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdeliver.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(UserDetailsBlueprint)

    return app
