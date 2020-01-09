import json
from datetime import datetime, timedelta
from typing import List, Any

from py_modules import backend_api
from py_modules.db_api import DBApi
from py_modules.imap_api import ImapApi


class MailApi:
    def __init__(self, uuid=-1):
        self.uuid = uuid
        self.userId = backend_api.get_user_id()

    @staticmethod
    def read_json_data_from_fs(uid):
        # @todo: read the json data, return a dict
        with open('.db/mails/' + str(uid) + '.json', 'r') as f:
            return json.load(f)

    def get_attach_info_from_db(self, uid):
        datastream: List[Any] = DBApi("attach").get_files_information(uid=uid, user_id=self.userId)
        files = []
        for file in datastream:
            files.append({
                "filename": file[0],
                "deleted": file[1]
            })
        return files

    def get_mails(self, days):
        if days == 0:
            ImapApi().get_today_mails()

        # return mails day by day
        d = datetime.today() - timedelta(days=days)
        mails: List[Any] = DBApi("mails").get_mail(date=d, user_id=self.userId)

        # now we need to create the dict
        dict_mails = []
        for mail in mails:
            # Getting json info
            # read file
            with open(".db/mails/" + str(mail[1]) + ".json", "r") as myfile:
                data = myfile.read()

            # parse file
            obj = json.loads(data)

            # getting attach info
            self.get_attach_info_from_db(mail[0])

            # Creating the dict
            tempmail = {
                "uid": mail[1],
                "From_name": str(obj['From_name']),
                "from_mail": str(obj['from_mail']),
                "To_name": str(obj['To_name']),
                "To_mail": str(obj['To_mail']),
                "Subject": str(mail[2]),
                "bodyHTML": str(obj['bodyHTML']),
                "bodyPLAIN": str(obj['bodyPLAIN']),
                "attach": str(obj['attach']),
                "directory": str(mail[4]),
                "datetimes": str(mail[6]),
                "readed": str(mail[5]),
            }

            dict_mails.append(tempmail)

        return dict_mails


    def get_folder(self, foldername = "Inbox"):
        mails: List[Any] = DBApi("mails").get_mail(user_id=self.userId, folder=foldername)

        # now we need to create the dict
        dict_mails = []
        for mail in mails:
            # Getting json info
            # read file
            with open(".db/mails/" + str(mail[1]) + ".json", "r") as myfile:
                data = myfile.read()

            # parse file
            obj = json.loads(data)

            # getting attach info
            self.get_attach_info_from_db(mail[0])

            # Creating the dict
            tempmail = {
                "uid": mail[1],
                "From_name": str(obj['From_name']),
                "from_mail": str(obj['from_mail']),
                "To_name": str(obj['To_name']),
                "To_mail": str(obj['To_mail']),
                "Subject": str(mail[2]),
                "bodyHTML": str(obj['bodyHTML']),
                "bodyPLAIN": str(obj['bodyPLAIN']),
                "attach": str(obj['attach']),
                "directory": str(mail[4]),
                "datetimes": str(mail[6]),
                "readed": str(mail[5]),
            }

            dict_mails.append(tempmail)

        return dict_mails

