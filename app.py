#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function  # For Py2/3 compatibility

import datetime
import json
import logging
import re
# import python smtplib module
import smtplib
import socket
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import eel
# import python imaplib wrapper module
from imbox import Imbox

from py_modules import backend_api
from py_modules import db_api

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.CRITICAL,
)

# Set web files folder
eel.init("web")





def mail_parsing(uid, message, unread_uid, directory):
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
        db_api.insert("files", payload)

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
    db_api.insert("mails", mail_payload)

    return appmails


@eel.expose
def check_smtp_connection(username, password, smtp):
    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = username
    msg["Subject"] = "Weclome in ToooMail"
    msg.attach(MIMEText("Hey! We're glad you're here!"))

    try:
        print("sending mail to " + username + " on " + "Welcome in ToooMail")

        mailServer = smtplib.SMTP(smtp, 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
        mailServer.sendmail(username, username, msg.as_string())
        mailServer.close()
        return True

    except Exception as e:
        print(str(e))
        return False


@eel.expose
def check_imap_connection(email, passw, imap):
    try:
        with Imbox(
            imap,
            username=email,
            password=passw,
            ssl=True,
            ssl_context=None,
            starttls=False,
        ) as imbox:
            imbox.messages()
        return True
    except Exception as e:
        return False


@eel.expose
def get_mails(year, month, day):
    # Download all the mails from the DB
    # backend_api.get_mails(year,month,day)
    # mails = db_api.get("emails","*","WHERE datetimes = "+datetime.date(year, month, day))

    mails = []
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account informations correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(date__on=datetime.date(year, month, day))
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug("Gathered all inbox messages")

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, "inbox")
            # saving the mail in the local FS (file system)
            with open("./.db/mails/" + str(uid.decode()) + ".json", "w") as file:
                json.dump(mail, file)

            mails.append(mail)

        return mails


@eel.expose
def mark_as_seen(uid):
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:
        imbox.mark_seen(uid)


@eel.expose
def get_number_unread():
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:
        logging.info("Account informations correct. Connected.")

        # Gets all messages after the day x

        # to get the mails of today:
        all_unread_message = imbox.messages(unread=True)
        return len(all_unread_message)


@eel.expose
def get_unread():
    mails = []
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account informations correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(unread=True)
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug("Gathered all inbox messages")

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, "Unread")
            mails.append(mail)

        return mails


@eel.expose
def get_starred():
    mails = []
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account information correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(flagged=True)
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug("Gathered all inbox messages")

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, "Flagged")
            mails.append(mail)

        return mails


@eel.expose
def get_sent():
    mails = []
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account information correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(sent_from=username)
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug("Gathered all inbox messages")

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, "Sent")
            mails.append(mail)

        return mails


@eel.expose
def get_unwanted():
    mails = []
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account information correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(folder="Junk")
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug("Gathered all inbox messages")

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, "Junk")
            mails.append(mail)

        return mails


@eel.expose
def get_deleted():
    mails = []
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account information correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(folder="Deleted")
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug("Gathered all inbox messages")

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, "Deleted")
            mails.append(mail)

        return mails


@eel.expose
def send_mail(account, to, subject, body, attach):
    # get user input
    # input sender email address and password:
    from_addr = backend_api.get_user_info("mail")
    password = backend_api.get_user_info("password")
    # input receiver email address.
    to_addr = to
    # input smtp server ip address:
    smtp_server = backend_api.get_user_info("smtpserver")

    # email object that has multiple part:
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = Header(subject, "utf-8").encode()

    # attache a MIMEText object to save email content
    msg_content = MIMEText(body, "plain", "utf-8")
    msg.attach(msg_content)

    # to add an attachment is just add a MIMEBase object to read a picture locally.
    # extracting list of attach from the attach object (vector)
    """with open('/Users/jerry/img1.png', 'rb') as f:
        # set attachment mime and file name, the image type is png
        mime = MIMEBase('image', 'png', filename='img1.png')
        # add required header data:
        mime.add_header('Content-Disposition', 'attachment', filename='img1.png')
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', '<0>')
        # read attachment file content into the MIMEBase object
        mime.set_payload(f.read())
        # encode with base64
        encoders.encode_base64(mime)
        # add MIMEBase object to MIMEMultipart object
        msg.attach(mime)
        
        'smtp-mail.outlook.com'
        """

    mailServer = smtplib.SMTP(backend_api.get_user_info("imapserver"), 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(
        backend_api.get_user_info("mail"), backend_api.get_user_info("password")
    )
    mailServer.sendmail(account, to, msg.as_string())
    mailServer.close()


@eel.expose
def get_flagged():
    mails = []
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account information correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(flagged=True)
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug("Gathered all inbox messages")

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, "Flagged")
            mails.append(mail)

        return mails


@eel.expose
def delete_mail(uid):
    db_api.delete("mails", uid, "")
    backend_api.update_mails()


@eel.expose
def add_note(text, uid, attach):
    db_api.insert("notes", {"uid": uid, "attach": attach})


@eel.expose
def del_note(uid):
    db_api.delete("notes", uid)


@eel.expose
def add_contact(name, surname, mail, note, nick):
    db_api.insert(
        "contact",
        {"name": name, "surname": surname, "mail": mail, "note": note, "nick": nick},
    )


@eel.expose
def get_contacts():
    pass


@eel.expose
def event():
    # notify the frontend for incoming events
    pass


@eel.expose
def set_user(name, nick, mail, passw, imapserver, smtpserver):
    db_api.insert(
        "user",
        {
            "name": name,
            "surname": "",
            "nickname": nick,
            "bio": "",
            "mail": mail,
            "password": passw,
            "profilepic": "",
            "imapserver": imapserver,
            "smtpserver": smtpserver,
            "datetime": datetime.datetime.now(),
        },
    )


@eel.expose
def set_flag(uid):
    return True


@eel.expose  # Expose this function to Javascript
def say_hello_py(x):
    print("Hello from %s" % x)


@eel.expose
def guess_imap(mail):
    """This function tries to find the imap/smtp address from a list of known servers
        or tries to guess the server from the e-mail address.
        It checks if the server answers to a socket call"""
    if mail:
        domain = re.search(r"(@)(.*)(\.)", mail).group(2)
        complete_domain = re.search(r"(@)(.*\..*)", mail).group(2)
    else:
        return False
    server = {
        "gmail": "imap.gmail.com",
        "yahoo": "imap.mail.yahoo.com",
        "aol": "imap.aol.com",
        "icloud": "imap.mail.me.com",
        "me": "imap.mail.me.com",
        "hotmail": "imap-mail.outlook.com",
        "live": "imap-mail.outlook.com",
    }
    if domain in server.keys():
        return server[domain]
    else:
        ip = None
        prefix = ["mail.", "imap.", "imap.mail.", "imap-mail."]
        for i in prefix:
            try:
                connection = socket.create_connection(
                    (i + complete_domain, 993), timeout=2
                )
                if connection:
                    ip = i + complete_domain
                    connection.close()
                    return ip
            except:
                pass
            if ip:
                return ip
            else:
                return False


@eel.expose
def guess_smtp(mail):
    """This function tries to find the imap/smtp address from a list of known servers
        or tries to guess the server from the e-mail address.
        It checks if the server answers to a socket call"""
    if mail:
        domain = re.search(r"(@)(.*)(\.)", mail).group(2)
        complete_domain = re.search(r"(@)(.*\..*)", mail).group(2)
    else:
        return False
    server = {
        "gmail": "smtp.gmail.com",
        "yahoo": "smtp.mail.yahoo.com",
        "aol": "smtp.aol.com",
        "icloud": "smtp.mail.me.com",
        "me": "smtp.mail.me.com",
        "hotmail": "smtp-mail.outlook.com",
        "live": "smtp-mail.outlook.com",
    }
    if domain in server.keys():
        return server[domain]
    else:
        ip = None
        prefix = ["mail.", "smtp.", "smtp.mail.", "smtp-mail."]
        for i in prefix:
            try:
                connection = socket.create_connection(
                    (i + complete_domain, 465), timeout=2
                )
                if connection:
                    ip = i + complete_domain
                    connection.close()
                    return ip
            except:
                pass
            if ip:
                return ip
            else:
                return False


# DA SPOSTARE SU THREAD DEDICATO
def download_every_email():
    username = backend_api.get_user_info("mail")
    passw = backend_api.get_user_info("password")
    imapserver = backend_api.get_user_info("imapserver")
    with Imbox(
        imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False,
    ) as imbox:

        logging.info("Account information correct. Connected.")

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages()
        logging.debug("Downloading every mail from the server")

        i = 0
        print(all_inbox_messages.__len__())
        for uid, message in reversed(all_inbox_messages):
            # Check if the mail exists in the local database
            percentage = i / all_inbox_messages.__len__()
            print(percentage * 100)
            print(i)
            print(db_api.get("mails", "uuid", "WHERE uuid =" + uid.decode()))
            i = i + 1
            query = db_api.get("mails", "uuid", "WHERE uuid =" + uid.decode())
            if not query:
                try:
                    print("DOWNLOADING THE MAIL")
                    mail_parsing(uid, message, "1", "Inbox")
                except Exception as e:
                    pass


if __name__ == "__main__":
    say_hello_py("Server.")
    eel.say_hello_js("Server connected.")  # Call a Javascript function

    template = check_if_user_exists()

    eel.start(template, mode="electron")  # Start
