import unittest
from app import *

from py_modules.db_api import DBApi
from py_modules.user_api import UserApi


class TestStringMethods(unittest.TestCase):
    def test__user_info(self):
        self.assertEqual(check_smtp_connection("false", "false", "false"), False)

    def test__user_exist(self):
        self.assertEqual(UserApi.check_if_user_exists(), "registration.html")

    def test__data_get(self):
        self.assertEqual(DBApi("user").get("id", "WHERE ID = 1"), [])


if __name__ == "__main__":
    unittest.main()
