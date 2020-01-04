from py_modules import backend_api
from py_modules.db_api import DBApi
from py_modules.imap_api import ImapApi


class SYNCApi:
    __userId = 1

    def __init__(self):
        """SYNCApi - Sync between local db and remote server.
        This utility must run
        on a dedicated thread."""
        # @todo: add a custom queue to upload changes to the server
        self.__userId = backend_api.get_user_id()

    def download_new_mails_from_server(self):
        """This func download new mails from the server and
        save them in the local database"""

        # Getting the last email uid
        last_mail_id = DBApi().get_last_email_id(user_id=self.__userId)

        # Getting new mails and saving them in the local db
        ImapApi().save_greater_than_uuid_from_server(uuid=last_mail_id)
