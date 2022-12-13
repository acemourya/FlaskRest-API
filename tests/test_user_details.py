import os
import unittest
import requests
from dotenv import load_dotenv
from tests.user_utils import UserUtils


class TestUserDetails(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        load_dotenv()
        cls.url = os.getenv('URL')
        cls.user_data = UserUtils().read_file(os.getenv('USER_DATA_FILE'))
        cls.user_details = UserUtils().read_file(os.getenv('USER_DETAILS_FILE'))

    @classmethod
    def tearDownClass(cls):
        UserUtils.delete_user_details(os.getenv('USER_DETAILS_FILE'))

    def test_upload_file(self):

        response = requests.post(self.url + "upload", files=self.user_details)
        self.assertEqual(response.status_code, 200)

    def test_upload_no_file(self):
        response = requests.post(self.url + "upload", files="")
        self.assertEqual(response.status_code, 400)

    def test_upload_invalid_file_format(self):
        response = requests.post(self.url + "upload", files=self.user_data)
        self.assertEqual(response.status_code, 400)
