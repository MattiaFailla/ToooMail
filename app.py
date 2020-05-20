#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import smtplib
import time

import eel
from imbox import Imbox

import configuration
from py_modules.db_api import DBApi, DBHelper
from py_modules.imap_api import ImapApi
from py_modules.mail_api import MailApi
from py_modules.smtp_api import SMTPApi
from py_modules.sync_api import SYNCApi
from py_modules.user_api import UserApi

logger = configuration.get_current().logger

# Set web files folder
# eel.init('ui') # Used to develop the frontend in a separate environment
eel.init('web')


@eel.expose
def check_smtp_connection(mail_address, password, smtp):
    """
    This function, mainly used in registration, is helpful to verify smtp settings
    :param mail_address: The username for the smtp server.
    :param password: The password of the account
    :param smtp: The smtp server address
    :return: The success of the connection as Boolean
    """
    try:
        logger.debug(f'Sending mail to {mail_address} on Welcome in ToooMail')

        mail_server = smtplib.SMTP(smtp, 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(mail_address, password)
        mail_server.close()
        return True

    except Exception as e:
        # FIXME: Catch only specific exceptions if possible
        logger.error('Error during smtp connection check', e)
        return False


@eel.expose
def check_imap_connection(email, passw, imap, ssl_field, ssl_context_field, starttls_field):
    """
    This function mainly used in registration is helpful to verify the imap setting
    :param email: The mail as String
    :param passw: The password as String
    :param imap: The imap server address as String
    :param ssl_field: The ssl flag.
    :param ssl_context_field: The ssl_context flag
    :param starttls_field: The starttls flag
    :return: The success of the connection as Boolean
    """
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
    """
    This function return a list of 'step' length of emails for the Inbox
    :param step: The number of emails as Int
    :return: The list of emails
    """
    # days -> number of days to be - from today
    return MailApi().get_mails(step=step)


@eel.expose
def get_mail_by_uuid(uuid):
    """
    This function return the mail payload for the given mail id.
    :param uuid: The mail id
    :return: The mail detail as a Dictionary
    """
    return MailApi().get_specific_email(uuid=uuid)


@eel.expose
def mark_as_seen(uid):
    """
    This function mark as seen the given mail uid.
    :param uid: The uid of the email
    :return: Success as boolean
    """
    SYNCApi.mark_as_seen(uid=str(uid))
    return True


def mark_flag(uid):
    """
    This function flag an email.
    :param uid: The id of the mail
    :return: Success as boolean
    """
    SYNCApi.mark_flag(uid=str(uid))
    return True


@eel.expose
def get_number_unread():
    """
    This function returns the number of unread emails.
    :return: The number of unread emails as Int
    """
    return SYNCApi().get_number_unread()


@eel.expose
def get_unread():
    # @ TODO: Move this function to imapApi lib
    """mails = []
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

        return mails"""


# FROM FOLDER
@eel.expose
def get_starred():
    """
    This function returns the list of starred emails
    :return: The list of dictionary of starred emails.
    """
    SYNCApi.get_folder(folder_name='Starred')
    return MailApi().get_folder('Starred')


@eel.expose
def get_unwanted():
    """
    This function returns the list of unwanted emails
    :return: The list of dictionary of unwanted emails.
    """
    SYNCApi.get_folder(folder_name='Junk')
    return MailApi().get_folder('Junk')


@eel.expose
def get_deleted():
    """
    This function returns the list of deleted emails
    :return: The list of dictionary of deleted emails.
    """
    SYNCApi.get_folder(folder_name='Deleted')
    return MailApi().get_folder('Deleted')


# FROM :SPECIFICS:
@eel.expose
def get_flagged():
    """
    This function returns the list of flagged emails
    :return: The list of dictionary of flagged emails.
    """
    SYNCApi.get_flagged()
    return MailApi().get_folder('Flagged')


@eel.expose
def get_sent():
    """
    This is the primary way for the frontend to receive the list pf Sent emails.
    :return: The list of dictionary of sent emails.
    """
    SYNCApi.get_sent()
    return MailApi().get_folder('Sent')


@eel.expose
def delete_mail(uid):
    """
    This function provide the deletion of the gived uid both in local and remote.
    :param uid: The uid of the mail
    :return: Success as boolean
    """
    # @todo: delete the mail both local and remote
    DBApi('mails').delete(what=uid, where='uuid')
    return True


@eel.expose
def add_note(text, uid, attach):
    """
    This function provide the addition of a note for the gived uid
    :param text: The text of the note as String.
    :param uid: The uid of the mail as Int.
    :param attach: The list of attachments
    :return: None
    """
    DBApi('notes').insert({'uid': uid, 'attach': attach, 'text': text})


@eel.expose
def del_note(uid):
    """
    This function provide the deletion of a note for a given mail uid.
    :param uid: The mail uid as int
    :return: None
    """
    DBApi('notes').delete(what=uid, where='')


@eel.expose
def add_contact(name, surname, mail, note, nick):
    """
    This function provide an easy way to save a contact.
    :param name: The name of the contact as String.
    :param surname: The surname (if any) ot the contact as String
    :param mail: The mail of the contact
    :param note: Notes (if any) for the contact.
    :param nick: The nick (if any) for the contact
    :return: None
    """
    DBApi('contact').insert({'name': name, 'surname': surname, 'mail': mail, 'note': note, 'nick': nick})


@eel.expose
def get_contacts():
    """
    This is the primary way to extract the list of saved contacts.
    :return: List of dictionary of saved contacts.
    """
    # @todo: get the contacts list
    pass


@eel.expose
def user_registration(name, mail, passw, imapserver, smtpserver, mail_server_id):
    """
    This is the regular user registration. It simply accept all the given parameters and make a dictionary
    to be saved in the db.
    :param name: The username.
    :param mail: The mail address.
    :param passw: The account password.
    :param imapserver: The imap server address.
    :param smtpserver: The smtp server address.
    :param mail_server_id: The id of the selected platfrom (read the file in './configuration/mail_server.json')
    :return: Success as boolean.
    """
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
    ImapApi().get_today_mails()


@eel.expose
def custom_user_registration(name, mail, passw, imapserver, smtpserver, ssl, ssl_context, starttls):
    """
    This function provide the functionality for custom user and settings registration. This settings will
    be saved in the DB as custom settings.
    :param name: The username as String.
    :param mail: The email address as String.
    :param passw: The password as String.
    :param imapserver: The imap server address as String.
    :param smtpserver: The smtp server address as String.
    :param ssl: Boolean flag to set the SSL setting for the imap server.
    :param ssl_context: Boolean flag to set the ssl_context flag for the imap server.
    :param starttls: Boolean flag to set the starttls flag for the imap server.
    :return: Success as boolean
    """
    mail_server_id = DBHelper.insert_custom_registration(imapserver, smtpserver, ssl, ssl_context, starttls)
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
    return True


@eel.expose
def set_flag(uid):
    """
    This function is able to flag the specified email.
    :param uid: Int
    :return: Boolean as success flag.
    """
    # @TODO: Add a flag to the mail.
    return True


@eel.expose
def send_mail(subject, cc, to, body, attach=None):
    """
    This function simply provide an easy callable interface for SMTPApi to send emails.
    :param subject: The subject as String.
    :param cc: The cc as String.
    :param to: The recipient as String.
    :param body: The body of the mail in HTML, stripped in String for easy support.
    :param attach: The list of IOString of attachments.
    :return: None
    """
    SMTPApi().send_mail(subject, cc, to, body, attach)


@eel.expose  # Expose this function to Javascript
def say_hello_py(x):
    """
    This function is the primary function called in main and the scope is only to notify the correct startup of the app.
    :param x: Str
    :return: None
    """
    logger.info(f'Hello from {x}.')


@eel.expose
def get_email_platform_settings(id):
    """
    This function returns the server settings associated to a specific mail service id.
    :param id: Int
    :return: The list of Dictionary with the settings of the specified id.
    """
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
    """
    This function returns the list of email platforms currently supported by ToooMail.
    You can find the list of supported setting in './configuration/mail_server.json'.
    :return: The list of Dictionary of current supported mail services.
    """
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
def guess_imap(user, passwrd, server):
    """
    This function tries to guess the imap server settings tring to
    connect with usual standard settings starting from the more secure
    :param server: The server name as a string
    :param passwrd: Password for the user4
    :param user: Username as a string
    :type user: str
    :type passwrd: str
    :type server: str
    :return: A dictionary with the element 'success' as boolean and the element 'settings' as a dictionary of settings
    for the connection
    """
    # possible settings: ssl, tls
    settings = [
        (True, True),
        (False, True),
        (True, False),
        (False, False)
    ]
    for i in settings:
        try:
            connection = Imbox(
                server,
                username=user,
                password=passwrd,
                ssl=i[0],
                starttls=i[1],
                ssl_context=None
            )
            test = connection.connection.check()
            logger.debug(f'guess for {server}, result {test}')
            if test[0] == 'OK':
                setting = {
                    'port': connection.server.port,
                    'ssl': i[0],
                    'starttls': i[1],
                    'ssl_context': None,
                    'server': connection.hostname,
                    'user': connection.username,
                    'password': connection.password
                }
                connection.logout()
                return {'success': True, 'settings': setting}
        except Exception as e:
            pass
        time.sleep(2.0)
    return {'success': False, 'settings': None}


@eel.expose
def guess_smtp(server):
    """
    This function tries to find the smtp settings using the more common ports.
    :param server: The name of the target server as a String
    :type server: str
    :return: A dictionary with the element 'success' as boolean and the element 'settings' as a dictionary
    that contains the 'port' number and 'ssl' or 'tls' as cryptographic protocol
    """
    ports = [
        25,
        587,
        465
    ]
    for i in ports:
        try:
            connection = smtplib.SMTP(server, i)
            res = connection.starttls()
            connection.close()
            if res[0] == 220:
                return {'success': True, 'settings': {'port': i, 'tls': True}}
        except:
            pass
        try:
            connection = smtplib.SMTP_SSL(server, i)
            res = connection.ehlo()
            connection.close()
            if res[0] == 250:
                return {'success': True, 'settings': {'port': i, 'ssl': True}}
        except:
            pass
    return {'success': False, 'settings': None}


@eel.expose
def get_username():
    """
    This function provide the username by accessing the UserApi class.
    :return: Str
    """
    return UserApi.get_username()


def sync():
    """
    This function provide an interface for SYNCApi sync method.
    :return: None
    """
    logger.info("Starting sync in separate thread.")
    SYNCApi().download_new_mails_from_server()


def download_from_latest_datetime():
    """
    This function starts the download of the Inbox from the latest saved mail datetime in the database.
    It's an easy and dirty way to keep the local version synced with the remote server.
    :return: None
    """
    logger.debug("Starting today mail download in separate thread.")
    ImapApi().download_mails_from_last_saved_datetimemail()
    logger.info("Sync of the current day completed.")


@eel.expose
def pong() -> str:
    """
    This function provide an easy way for the frontend to keep the websocket alive.
    :rtype: basestring
    """
    return "ping"


@eel.expose
def ui_log(message: str) -> None:
    """
    This function provide the integration with Tentalog for easy logging from the frontend.
    :param message: str
    :return: None
    """
    logger.debug(f'UI: {message}')


@eel.expose
def ui_log_error(message: str) -> None:
    """
    This function provide the functionality to log an error from the frontend.
    :param message: str
    :return: None
    """
    logger.error(f'UI: {message}')


def check_incoming():
    """
    Polling the server for incoming emails every 30 second on a separate thread.
    :return: ToooMail.internals.notification
    """
    while True:
        last_uid, new_emails_number = ImapApi().check_new_emails()
        if new_emails_number > 0:
            logger.info(f'Numero di nuove mail {new_emails_number}')
            logger.debug(f' Ultimo UID: {last_uid}')
            # ImapApi().save_greater_than_uuid_from_server(last_uid)
        eel.sleep(30.0)  # Use eel.sleep(), not time.sleep()


def watcher():
    while True:
        logger.info('Checking the remote server for incoming emails.')
        ImapApi().mail_watcher()
        eel.sleep(20)


if __name__ == '__main__':
    say_hello_py('ToooMail server')

    # Starting the watcher on separate thread
    eel.spawn(watcher)

    # Downloading new emails
    download_from_latest_datetime()

    template = UserApi.check_if_user_exists()
    if template == 'index.html':
        eel.start(template, block=True, port=8686, mode=False)  # Start
    else:
        eel.start(template, block=True, port=8686)  # Start

    logger.info("Closing the app.")
