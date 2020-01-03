import sqlite3

from py_modules import backend_api


class UserApi:
    userId = ""
    userName = ""

    def __init__(self, userId, userName):
        self.userId = userId
        self.userName = userName

    def get_username(self):
        if self.userId:
            return self.userId
        else:
            return backend_api.get_user_info("mail")
    
    def get_user_id(self):
        return self.userId

    @staticmethod
    def check_if_user_exists():
        # if user isn't logged -> start the "subscription app" the first time
        conn = sqlite3.connect(".db/app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user;")
        # print(cursor.fetchall())
        if not cursor.fetchall():
            return "registration.html"
        else:
            return "index.html"

