import multiprocessing

from py_modules import backend_api
from py_modules.db_api import DBApi
from py_modules.imap_api import ImapApi


class SYNCApi:
    def __init__(self):
        """SYNCApi - Sync between local db and remote server.
        This utility must run
        on a dedicated thread."""
        # @todo: add a custom queue to upload changes to the server
        self.__userId = backend_api.get_user_id()

    def download_new_mails_from_server(self):
        """This func download new mails from the server and
        save them in the local database"""

        # @todo: get folder list -> download per folder (pool of download)

        # Getting the last email uid
        last_mail_id = DBApi().get_last_email_id(user_id=self.__userId)

        # Getting new mails and saving them in the local db
        ImapApi().save_greater_than_uuid_from_server(uuid=last_mail_id)

    def get_number_unread(self):
        imap = ImapApi().get_number_unread_from_server()
        db = DBApi().get_unopened()
        if imap > db:
            # we need to fetch new mails
            if multiprocessing.active_children() is None:
                p = multiprocessing.Process(target=self.download_new_mails_from_server(), args=())
                p.start()
        return imap

    def force_update(self):
        # @todo: this function run when the user force the update of the current day
        return

    @staticmethod
    def check_mails_for_today():
        # @todo: this function call ImapApi and try to save mails from today's folder
        ImapApi().get_today_mails()

    @staticmethod
    def mark_as_seen(uid):
        ImapApi().mark_as_seen(uid=uid)
        DBApi().mark_as_seen(uid=uid)

    @staticmethod
    def get_folder(folder_name):
        ImapApi().get_folder_mails_from_server(folder_name=folder_name)

    @staticmethod
    def get_flagged():
        ImapApi().get_flagged_messages()
        pass

    @staticmethod
    def get_sent():
        ImapApi.get_sent()



