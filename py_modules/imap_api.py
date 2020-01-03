import datetime

from imbox import Imbox

from py_modules.db_api import DBApi


def mail_parsing_from_server(uid, message, unread_uid, directory):
    """
    This function clean, parse and save a mail in the local filesystem.
    """
    if len(message.body["html"]) < 1:
        sanitized_body = str(message.body["plain"][0])
    else:
        sanitized_body = str(message.body["html"][0])

    from_name = message.sent_from[0]["name"] if message.sent_from else ""
    from_mail = message.sent_from[0]["email"] if message.sent_from else ""
    to_name = message.sent_to[0]["name"] if message.sent_to else ""
    to_mail = message.sent_to[0]["email"] if message.sent_to else ""

    date_message = message.date

    # If html body is empty, load the plain
    if sanitized_body == "[]":
        sanitized_body = message.body["plain"]

    if uid.decode() in unread_uid:
        unread = False
    else:
        unread = True

    # Getting the subject
    subject = str(message.subject) if str(message.subject) else "(No subject)"

    # saving attach in the local disk and on the db
    attach_names = []
    for attach in message.attachments:
        attach_name = attach.get("filename")
        attach_names.append(attach_name)
        content = attach.get("content").read()

        if not attach_name or not content:
            return

        with open(".db/mails/attach/" + uid.decode() + "_" + attach_name, "wb") as file:
            file.write(content)
        payload = {
            "uuid": uid.decode(),
            "subject": subject,
            "real_filename": attach_name,
            "saved_as": uid.decode() + "_" + attach_name,
            "user_id": "1",
            "deleted": "false",
            "datetime": date_message,
        }
        # saving the file information into the db
        DBApi("files").insert(data=payload)

    appmails = {
        "uid": uid.decode(),
        "From_name": str(from_name),
        "from_mail": str(from_mail),
        "To_name": str(to_name),
        "To_mail": str(to_mail),
        "Subject": str(subject),
        "bodyHTML": str(sanitized_body),
        "bodyPLAIN": str(message.body["plain"]),
        "attach": attach_names,
        "directory": directory,
        "datetimes": str(""),
        "readed": unread,
    }

    # inserting the mail in the database
    mail_payload = {
        "uuid": uid.decode(),
        "subject": str(subject),
        "user_id": "1",
        "datetime": date_message,
    }

    DBApi("mails").insert(data=mail_payload)

    return appmails


class ImapApi:
    def __init__(self, userId, userName, password, server):
        self.userId = userId
        self.userName = userName
        self.password = password
        self.server = server
        # Getting the imap configuration
        self.ssl = True
        self.ssl_context = None
        self.starttls = False

    def check_imap_connection(self):
        """
        Checking if imap connection is successful
        """
        try:
            with Imbox(
                    self.server,
                    username=self.userName,
                    password=self.password,
                    ssl=self.ssl,
                    ssl_context=self.ssl_context,
                    starttls=self.starttls,
            ) as imbox:
                imbox.messages()
                return True
        except Exception as e:
            return False, e

    def get_inbox_from_server(self):
        """
        Getting inbox messages from the server
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            return imbox.messages()

    def get_folder_list_from_server(self):
        """
        Getting the list of folders on the server.
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            status, folders_with_additional_info = imbox.folders()
            return folders_with_additional_info

    def get_folder_mails_from_server(self, folder_name):
        """
        Getting the list of emails in a subfolder from the server.
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            return imbox.messages(folder=folder_name)

    def set_seen_on_server(self, uuid):
        """
        Setting a mail as seen on the server.
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            imbox.mark_seen(uuid)

    def get_unread_from_server(self):
        """
        Getting uuid of unread emails
        """
        mails = []
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            all_inbox_messages = imbox.messages(unread=True)
            unread_msgs = imbox.messages(unread=True)
            unread_uid = []
            for uid, msg in unread_msgs:
                unread_uid.append(uid.decode())

            for uid, message in reversed(all_inbox_messages):
                mail = mail_parsing_from_server(uid, message, unread_uid, "Unread")
                mails.append(mail)

            return mails

    def get_number_unread_from_server(self):
        """
        Getting the number of unread emails on the server
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            all_unread_message = imbox.messages(unread=True)
            return len(all_unread_message)

    def get_specific_mail_subject(self, given_subject):
        """
        Getting a set of emails on a given subject
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            parsed_mails = []
            mails = imbox.messages(subject=given_subject)
            for uid, mail in mails:
                parsed_mails.append(mail_parsing_from_server(uid, mail, "1", ""))

            return parsed_mails

    def get_specific_mail_datetime(self, year, month, day):
        """
        Getting a set of emails on a given datetime
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            parsed_mails = []
            mails = imbox.messages(date__on=datetime.date(year, month, day))
            for uid, mail in mails:
                parsed_mails.append(mail_parsing_from_server(uid, mail, "1", ""))

            return parsed_mails

    def get_flagged_messages(self):
        """
        Getting flagged emails from remote server.
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            parsed_mails = []
            mails = imbox.messages(flagged=True)
            for uid, mail in mails:
                parsed_mails.append(mail_parsing_from_server(uid, mail, "1", "Flagged"))

            return parsed_mails

    def delete_message_on_server(self, uuid):
        """
        Deleting a mail on the remote server.
        """
        with Imbox(
                self.server,
                username=self.userName,
                password=self.password,
                ssl=self.ssl,
                ssl_context=self.ssl_context,
                starttls=self.starttls,
        ) as imbox:
            imbox.delete(uuid)
            return True
