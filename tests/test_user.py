import os
import json
import unittest
import requests
from dotenv import load_dotenv
from tests.user_utils import UserUtils


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        load_dotenv()
        file_data = UserUtils().read_file(os.getenv('USER_DATA_FILE'))
        cls.url = os.getenv('URL')
        cls.user_data = json.loads(file_data['file'])

    @classmethod
    def tearDownClass(cls):
        UserUtils.delete_registered_user_cred(
            username=cls.user_data['user_register_cred']['username'])

    def test_registration(self):
        response = requests.post(
            self.url + "register", json=self.user_data['user_register_cred'])
        self.assertEqual(response.status_code, 200)

    def test_regiration_with_invalid_data(self):

        response = requests.post(
            self.url + "register", json=self.user_data['user_resgister_invalid_cred'])
        self.assertEqual(response.status_code, 400)

    def test_registration_with_existing_user(self):

        response = requests.post(
            self.url + "register", json=self.user_data['user_register_existing_cred'])
        self.assertEqual(response.status_code, 400)

    def test_registration_with_invalid_cred(self):

        response = requests.post(
            self.url + "register", json=self.user_data['user_resgister_wrong_cred'])
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        response = requests.post(
            self.url + "login", json=self.user_data['user_login_cred'])
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid(self):

        response = requests.post(
            self.url + "login", json=self.user_data['user_login_invaild_cred'])
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong(self):

        response = requests.post(
            self.url + "login", json=self.user_data['user_login_wrong_cred'])
        self.assertEqual(response.status_code, 400)
