#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json
import logging
import re
import smtplib
import socket
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import eel
# import python imaplib wrapper module
from imbox import Imbox

from py_modules import backend_api
from py_modules.db_api import DBApi
from py_modules.imap_api import ImapApi
from py_modules.mail_api import MailApi
from py_modules.sync_api import SYNCApi
from py_modules.user_api import UserApi

import multiprocessing
import configuration

logger = configuration.get_current().logger

# Set web files folder
# eel.init('ui')
eel.init('web')


def mail_parsing(uid, message, unread_uid, directory):
    if len(message.body['html']) < 1:
        sanitized_body = str(message.body['plain'][0])
    else:
        sanitized_body = str(message.body['html'][0])

    from_name = message.sent_from[0]['name'] if message.sent_from else ''
    from_mail = message.sent_from[0]['email'] if message.sent_from else ''
    to_name = message.sent_to[0]['name'] if message.sent_to else ''
    to_mail = message.sent_to[0]['email'] if message.sent_to else ''

    date_message = message.date

    # If html body is empty, load the plain
    if sanitized_body == '[]':
        sanitized_body = message.body['plain']

    if uid.decode() in unread_uid:
        unread = False
    else:
        unread = True

    # Getting the subject
    subject = str(message.subject) if str(message.subject) else '(No subject)'

    # saving attach in the local disk and on the db
    attach_names = []
    for attach in message.attachments:
        attach_name = attach.get('filename')
        attach_names.append(attach_name)
        content = attach.get('content').read()

        if not attach_name or not content:
            return

        with open('.db/mails/attach/' + uid.decode() + '_' + attach_name, 'wb') as file:
            file.write(content)
        payload = {
            'uuid': uid.decode(),
            'subject': subject,
            'real_filename': attach_name,
            'saved_as': uid.decode() + '_' + attach_name,
            'user_id': '1',
            'deleted': 'false',
            'datetime': date_message,
        }
        # saving the file information into the db
        DBApi('files').insert(data=payload)

    appmails = {
        'uid': uid.decode(),
        'From_name': str(from_name),
        'from_mail': str(from_mail),
        'To_name': str(to_name),
        'To_mail': str(to_mail),
        'Subject': str(subject),
        'bodyHTML': str(sanitized_body),
        'bodyPLAIN': str(message.body['plain']),
        'attach': attach_names,
        'directory': directory,
        'datetimes': str(''),
        'readed': unread,
    }

    # inserting the mail in the database
    mail_payload = {
        'uuid': uid.decode(),
        'subject': str(subject),
        'user_id': '1',
        'readed': date_message,
    }

    DBApi('mails').insert(data=mail_payload)

    with open('./.db/mails/' + str(uid.decode()) + '.json', 'w') as file:
        json.dump(appmails, file)

    return appmails


@eel.expose
def check_smtp_connection(username, password, smtp):
    try:
        logger.debug(f'Sending mail to {username} on Welcome in ToooMail')

        mail_server = smtplib.SMTP(smtp, 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(username, password)
        mail_server.close()
        return True

    except Exception as e:
        # FIXME: Catch only specific exceptions if possible
        logger.error('Error during smtp connection check', e)
        return False


@eel.expose
def check_imap_connection(email, passw, imap, ssl_field, ssl_context_field, starttls_field):
    try:
        with Imbox(
                imap,
                username=email,
                password=passw,
                ssl=ssl_field,
                ssl_context=ssl_context_field,
                starttls=starttls_field,
        ) as imbox:
            imbox.messages()
        return True
    except Exception as e:
        logger.error('Error during imap connection check', e)
        return False


@eel.expose
def get_mails(step):
    # days -> number of days to be - from today
    return MailApi().get_mails(step=step)


@eel.expose
def get_mail_by_uuid(uuid):
    return MailApi().get_specific_email(uuid=uuid)


@eel.expose
def mark_as_seen(uid):
    SYNCApi.mark_as_seen(uid=str(uid))
    return True


@eel.expose
def get_number_unread():
    return SYNCApi().get_number_unread()


@eel.expose
def get_unread():
    mails = []
    username = backend_api.get_user_info('mail')
    passw = backend_api.get_user_info('password')
    imapserver = backend_api.get_user_info('imapserver')
    with Imbox(
            imapserver,
            username=username,
            password=passw,
            ssl=True,
            ssl_context=None,
            starttls=False,
    ) as imbox:

        logging.info('Account informations correct. Connected.')

        # Gets all messages after the day x
        all_inbox_messages = imbox.messages(unread=True)
        unread_msgs = imbox.messages(unread=True)
        unread_uid = []
        for uid, msg in unread_msgs:
            unread_uid.append(uid.decode())
        logging.debug('Gathered all inbox messages')

        for uid, message in reversed(all_inbox_messages):
            mail = mail_parsing(uid, message, unread_uid, 'Unread')
            mails.append(mail)

        return mails


# FROM FOLDER
@eel.expose
def get_starred():
    SYNCApi.get_folder(folder_name='Starred')
    return MailApi().get_folder('Starred')


@eel.expose
def get_unwanted():
    SYNCApi.get_folder(folder_name='Junk')
    return MailApi().get_folder('Junk')


@eel.expose
def get_deleted():
    SYNCApi.get_folder(folder_name='Deleted')
    return MailApi().get_folder('Deleted')


# FROM :SPECIFICS:
@eel.expose
def get_flagged():
    SYNCApi.get_flagged()
    return MailApi().get_folder('Flagged')


@eel.expose
def get_sent():
    SYNCApi.get_sent()
    return MailApi().get_folder('Sent')


@eel.expose
def delete_mail(uid):
    # @todo: delete the mail both local and remote
    DBApi('mails').delete(what=uid, where='')


@eel.expose
def add_note(text, uid, attach):
    DBApi('notes').insert({'uid': uid, 'attach': attach, 'text': text})


@eel.expose
def del_note(uid):
    DBApi('notes').delete(what=uid, where='')


@eel.expose
def add_contact(name, surname, mail, note, nick):
    DBApi('contact').insert({'name': name, 'surname': surname, 'mail': mail, 'note': note, 'nick': nick})


@eel.expose
def get_contacts():
    # @todo: get the contacts list
    pass


@eel.expose
def event():
    # notify the frontend for incoming events
    # @todo: send a notification
    pass


@eel.expose
def user_registration(name, mail, passw, imapserver, smtpserver, mail_server_id):
    # Regular user registration
    data = {
        'name': name,
        'surname': '',
        'nickname': '',
        'bio': '',
        'mail': mail,
        'password': passw,
        'profilepic': '',
        'imapserver': imapserver,
        'smtpserver': smtpserver,
        'is_logged_in': True,
        'mail_server_setting': mail_server_id,
        'created': datetime.datetime.now().isoformat(),
    }
    UserApi.user_registration(datagram=data)


@eel.expose
def custom_user_registration(name, mail, passw, imapserver, smtpserver, ssl, ssl_context, starttls):
    # @todo set custom imap settings on the server and get id
    return True


@eel.expose
def set_flag(uid):
    # @todo: set flag remote and local!
    return True


@eel.expose
def send_mail(account, to, subject, body, attach):
    # get user input
    # input sender email address and password:
    from_address = backend_api.get_user_info('mail')
    password = backend_api.get_user_info('password')
    # input receiver email address.
    to_address = to
    # input smtp server ip address:
    smtp_server = backend_api.get_user_info('smtpserver')

    # email object that has multiple part:
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = Header(subject, 'utf-8').encode()

    # attache a MIMEText object to save email content
    msg_content = MIMEText(body, 'plain', 'utf-8')
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

    mail_server = smtplib.SMTP(backend_api.get_user_info('imapserver'), 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(
        backend_api.get_user_info('mail'), backend_api.get_user_info('password')
    )
    mail_server.sendmail(account, to, msg.as_string())
    mail_server.close()


@eel.expose  # Expose this function to Javascript
def say_hello_py(x):
    logger.info(f'Hello from {x}.')


@eel.expose
def get_email_platform_settings(id):
    result = DBApi('mail_server_settings').get(field='*', expression=f'WHERE ID = {str(id)}')
    fe_data = []
    for data in result:
        fe_data.append(
            {
                'id': data[0],
                'name': data[1],
                'smtp': data[2],
                'imap': data[3],
                'ssl': data[4],
                'sslcontext': data[5],
                'starttls': data[6],
            }
        )
    return fe_data


@eel.expose
def get_email_platform():
    # Getting vendors with ID
    result = DBApi('mail_server_settings').get(field='id, service_name', expression='')
    fe_data = []
    for data in result:
        fe_data.append(
            {
                'id': data[0],
                'name': data[1]
            }
        )
    return fe_data


@eel.expose
def guess_imap(mail):
    '''This function tries to find the imap/smtp address from a list of known servers
        or tries to guess the server from the e-mail address.
        It checks if the server answers to a socket call'''
    if mail:
        try:
            domain = re.search(r'(@)(.*)(\.)', mail).group(2)
            complete_domain = re.search(r'(@)(.*\..*)', mail).group(2)
        except Exception as e:
            # FIXME: catch specific exceptions instead of Exception
            logger.error('Error guessing imap', e)
            return False
    else:
        return False
    server = {
        'gmail': 'imap.gmail.com',
        'yahoo': 'imap.mail.yahoo.com',
        'aol': 'imap.aol.com',
        'icloud': 'imap.mail.me.com',
        'me': 'imap.mail.me.com',
        'hotmail': 'imap-mail.outlook.com',
        'live': 'imap-mail.outlook.com',
    }
    if domain in server.keys():
        return server[domain]
    else:
        ip = None
        prefix = ['mail.', 'imap.', 'imap.mail.', 'imap-mail.']
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
    """
    This function tries to find the imap/smtp address from a list of known servers
    or tries to guess the server from the e-mail address.
    It checks if the server answers to a socket call
    :param mail:
    :return:
    """
    if mail:
        try:
            domain = re.search(r'(@)(.*)(\.)', mail).group(2)
            complete_domain = re.search(r'(@)(.*\..*)', mail).group(2)
        except Exception as e:
            logger.error('Error guessing smtp', e)
            return False
    else:
        return False
    server = {
        'gmail': 'smtp.gmail.com',
        'yahoo': 'smtp.mail.yahoo.com',
        'aol': 'smtp.aol.com',
        'icloud': 'smtp.mail.me.com',
        'me': 'smtp.mail.me.com',
        'hotmail': 'smtp-mail.outlook.com',
        'live': 'smtp-mail.outlook.com',
    }
    if domain in server.keys():
        return server[domain]
    else:
        ip = None
        prefix = ['mail.', 'smtp.', 'smtp.mail.', 'smtp-mail.']
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


@eel.expose
def get_username():
    return UserApi.get_username()


def sync():
    SYNCApi().download_new_mails_from_server()


@eel.expose
def pong():
    return "ping"


@eel.expose
def ui_log(message):
    logger.debug(f'UI: {message}')


@eel.expose
def ui_log_error(message):
    logger.error(f'UI: {message}')


def check_incoming():
    while True:
        print("NEW EMAILS:")
        print(ImapApi().check_new_emails())
        eel.sleep(1.0)  # Use eel.sleep(), not time.sleep()


# eel.spawn(check_incoming) # FIXME

if __name__ == '__main__':
    say_hello_py('Server')
    # eel.say_hello_js('Server connected.')  # Call a Javascript function
    template = UserApi.check_if_user_exists()
    if template == 'index.html':
        """processes = [multiprocessing.Process(target=SYNCApi().download_new_mails_from_server, args=()) for x in
                     range(4)]"""

        eel.start(template, block=True, port=8686, mode=False)  # Start
    else:
        eel.start(template, block=True, port=8686)  # Start

    logger.info("Closing the app.")
