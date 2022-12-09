import os
import csv
from db import db
from flask import request, jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint
from models.user_details import UserDetails


blp = Blueprint("UserDetails", __name__,
                description="Store uploaded user file data in database")


@blp.route("/upload")
class UserDetiails(MethodView):

    def post(self):
        try:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save('./data.csv')
                if self.parseCSV():
                    return make_response(jsonify(message="Successfully uploaded file"), 200)
            return make_response(jsonify(message="Failed to upload file! Please try again"), 400)
        except:
            return make_response(jsonify(message="Failed to upload file"), 400)

    def parseCSV(self):
        try:
            with open('./data.csv', 'r') as csvfile:
                csvData = csv.DictReader(csvfile)
                for row in csvData:
                    userData = UserDetails(
                        username=row['Username'], email=row['Email'], phone=row['Phone'], address=row['Address'])
                    db.session.add(userData)
                    db.session.commit()
            os.remove('./data.csv')
            return True
        except:
            return False
