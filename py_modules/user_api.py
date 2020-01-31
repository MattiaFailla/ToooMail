import sqlite3
import configuration
from py_modules.db_api import DBApi

current_configuration = configuration.get_current()
logger = current_configuration.logger


class UserApi:
    def __init__(self):
        self.user_id = self.get_user_id()
        self.user_name = self.get_username()

    @staticmethod
    def user_registration(datagram):
        DBApi('user').insert(data=datagram)

    @staticmethod
    def check_if_user_exists():
        # if user isn't logged -> start the 'subscription app' the first time
        try:
            # Creating the sqlite3 database
            conn = sqlite3.connect(current_configuration)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM user;')
            if not cursor.fetchall():
                # UPLOADING THE CONFIG IN THE DB
                return 'registration.html'
            else:
                return 'index.html'
        except sqlite3.OperationalError as error:
            logger.critical('The db file is not present', error)

    @staticmethod
    def get_user_id():
        data = DBApi('user').get('id', 'WHERE is_logged_in = 1')
        p = data[0]
        return p[0]

    @staticmethod
    def get_username():
        data = DBApi('user').get('name', 'WHERE is_logged_in = 1')
        p = data[0]
        return p[0]
