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
        try:
            # Creating the sqlite3 database
            conn = sqlite3.connect(".db/app.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM user;")
            if not cursor.fetchall():
                # UPLOADING THE CONFIG IN THE DB
                return "registration.html"
            else:
                return "index.html"
        except sqlite3.OperationalError as error:
            print("IL FILE DB NON ESISTE, ERRORE FATALE")
            print(error)

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
