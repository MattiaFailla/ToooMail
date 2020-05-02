import datetime
from email.utils import parsedate_to_datetime
import json
from os import path
import dateutil.parser

from py_modules import backend_api
from py_modules.db_api import DBApi

import configuration

current_configuration = configuration.get_current()
logger = current_configuration.logger


class SMTPApi:
    def __init__(self):
        self.userId = backend_api.get_user_id()
        self.userName = backend_api.get_user_info("mail")
        self.password = backend_api.get_user_info("password")
        self.server = backend_api.get_user_server_config("server_smtp")

    def send_mail(self, subject, cc, to, body, attach):
        """ This function will send an email to the target email.

            :param subject: The subject of the mail.
            :param cc: The cc if any.
            :param to: The recipient.
            :param body: The body of the mail in HTML format.

            :param attach: The list of attachment paths
            :type attach: List
        """
