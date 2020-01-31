import json
import dateutil.parser
from typing import List, Any
import configuration
from py_modules import backend_api
from py_modules.db_api import DBApi
from py_modules.imap_api import ImapApi

current_configuration = configuration.get_current()
logger = current_configuration.logger


class MailApi:
    def __init__(self, uuid=-1):
        self.uuid = uuid
        self.user_id = backend_api.get_user_id()

    @staticmethod
    def read_json_data_from_fs(uid):
        # @todo: read the json data, return a dict
        with open('.db/mails/' + str(uid) + '.json', 'r') as f:
            return json.load(f)

    def get_attach_info_from_db(self, uid):
        data_stream = DBApi("attach").get_files_information(uid=uid, user_id=self.user_id)
        files = []
        for file in data_stream:
            files.append(file[0])
        return files

    def get_mails(self, step):
        ImapApi().get_today_mails()

        # return mails day by day
        step = step + 60
        mails: List[Any] = DBApi("mails").get_mail(step=step, user_id=self.user_id)

        # now we need to create the dict
        dict_mails = []
        for mail in mails:
            # Getting json info
            # read file
            try:
                with open(".db/mails/" + str(mail[1]) + ".json", "r") as my_file:
                    data = my_file.read()

                # parse file
                obj = json.loads(data)

                # getting attach info
                shipped_with = self.get_attach_info_from_db(mail[1])
                print(mail[1])
                # parsing datetime
                received = mail[6]
                parsed_date = dateutil.parser.parse(received)
                parsed_date = parsed_date.strftime("%d/%m/%Y %H:%M:%S")

                # Creating the dict
                temp_mail = {
                    "uid": mail[1],
                    "From_name": str(obj['From_name']),
                    "from_mail": str(obj['from_mail']),
                    "To_name": str(obj['To_name']),
                    "To_mail": str(obj['To_mail']),
                    "Subject": str(mail[2]),
                    "bodyHTML": str(obj['bodyHTML']),
                    "bodyPLAIN": str(obj['bodyPLAIN']),
                    "attach": obj['attach'],
                    "directory": str(mail[4]),
                    "datetimes": str(parsed_date),
                    "readed": str(mail[5]),
                }

                dict_mails.append(temp_mail)
            except Exception as e:
                logger.error('Error retrieving emails', e)

        return dict_mails

    def get_folder(self, folder_name="Inbox"):
        mails: List[Any] = DBApi("mails").get_mail(user_id=self.user_id, folder=folder_name)

        # now we need to create the dict
        dict_mails = []
        for mail in mails:
            # Getting json info
            # read file
            with open(".db/mails/" + str(mail[1]) + ".json", "r") as my_file:
                data = my_file.read()

            # parse file
            obj = json.loads(data)

            # getting attach info
            self.get_attach_info_from_db(mail[0])

            # Creating the dict
            temp_mail = {
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

            dict_mails.append(temp_mail)

        return dict_mails
