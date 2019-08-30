import unittest
from app import *

from py_modules import db_api


class TestStringMethods(unittest.TestCase):
    def test__user_info(self):
        self.assertEqual(verify_user_info("false", "false", "false"), False)

    def test__user_exist(self):
        self.assertEqual(check_if_user_exists(), "registration.html")

    def test__data_get(self):
        self.assertEqual(db_api.get("user", "id", "WHERE ID = 1"), [])


if __name__ == "__main__":
    unittest.main()
