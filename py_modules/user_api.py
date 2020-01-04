import sqlite3

from py_modules.db_api import DBApi


class UserApi:
    def __init__(self):
        self.userId = self.get_user_id()
        self.userName = self.get_username()

    @staticmethod
    def user_registration(datagram):
        DBApi("user").insert(data=datagram)

    @staticmethod
    def check_if_user_exists():
        # if user isn't logged -> start the "subscription app" the first time
        conn = sqlite3.connect(".db/app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user;")
        # print(cursor.fetchall())
        if not cursor.fetchall():
            # UPLOADING THE CONFIG IN THE DB
            DBApi.upload_config()
            return "registration.html"
        else:
            return "index.html"

    @staticmethod
    def get_user_id():
        data = DBApi("user").get("id", "WHERE is_logged_in = 1")
        p = data[0]
        return p[0]

    @staticmethod
    def get_username():
        data = DBApi("user").get("name", "WHERE is_logged_in = 1")
        p = data[0]
        return p[0]
