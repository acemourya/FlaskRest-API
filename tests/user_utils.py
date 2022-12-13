import logging
import csv
from models.user import User
from models.user_details import UserDetails
from db import db
from app import create_app


class UserUtils:

    def read_file(self, path):
        try:
            with open(path, 'rb') as f:
                files = {'file': f.read()}
            return files
        except:
            logging.error('Failed to read file')
            return

    def delete_registered_user_cred(username=None):
        try:
            with create_app().app_context():
                User.query.filter_by(username=username).delete()
                db.session.commit()
        except:
            logging.error('User data is not deleted')

    def delete_user_details(file_path=None):
        try:
            with create_app().app_context():
                with open(file_path, 'r') as data:
                    for user_details in csv.DictReader(data):
                        UserDetails.query.filter_by(
                            username=user_details['Username']).delete()
        except:
            logging.error('User details is not deleted')
