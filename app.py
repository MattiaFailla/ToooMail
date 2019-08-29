#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function	# For Py2/3 compatibility
import eel
import datetime
import sqlite3
import datetime
from imbox import Imbox

from py_modules import db_api
from py_modules import backend_api

import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.CRITICAL)

"""
**** feature

DISPALY MAILS
- Add widgets
- Fancy animation while removing the blue tick
- Correct number of unread mails
- Zoom on the image of the contact with contact informations (email, profile pic, name and notes)
- Add notes on the bottom of the mail
- Add spam icon and page
- Add a default image when the folder is empty (like unread or spam or flagged)
- Download the list of flagged emails

SEND MAILS
- Send the mail with smtp
- Load the attach
- Send mail at a certain time of the day/hour (slow send feature)

BACKEND
- Check the mails UID for incoming mails
- Add desktop notification
- Add an internal database and update that instaed of downloading the whole email pack every time
"""

"""
INVECE DI COMUNICARE DIRETTAMENTE CON IL FRONTED PASSIAMO TUTTO AL DB
"""

# Set web files folder
eel.init('web')

template = "index.html"

def check_if_user_exists():
	# if user isn't logged -> start the "subscription app" the first time
	conn = sqlite3.connect('db/app.db')
	cursor = conn.cursor()
	cursor.execute("SELECT id FROM user;")
	#print(cursor.fetchall())
	if not cursor.fetchall():
		return "registration.html"
	else:
		return "index.html"



@eel.expose
def verify_user_info(email,passw,imap):
	try:
		with Imbox(imap,
			username=email,
			password=passw,
			ssl=True,
			ssl_context=None,
			starttls=False) as imbox:
			imbox.messages()
		return True
	except Exception as e:
		return False

@eel.expose
def get_mails(year,month,day):
	# Download all the mails from the DB
	#backend_api.get_mails(year,month,day)
	#mails = db_api.get("emails","*","WHERE datetimes = "+datetime.date(year, month, day))

	mails = []
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x
		all_inbox_messages = imbox.messages(date__on=datetime.date(year,month,day))
		unread_msgs = imbox.messages(unread=True)
		unread_uid = []
		for uid, msg in unread_msgs:
			unread_uid.append(uid.decode())
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
			if sanitized_body == "[]":
				sanitized_body = str(message.body['plain'])
			sanitized_body = sanitized_body.replace(r"['\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"[b'", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r", "&#13;")
			sanitized_body = sanitized_body.replace(r"\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\t", "")
			sanitized_body = sanitized_body.replace(r"['", "")
			sanitized_body = sanitized_body.replace(r"']", "")

			# Apply local time to base server time
			From_name = message.sent_from[0]['name']
			From_mail = message.sent_from[0]['email']
			To_name = message.sent_to[0]['name']
			To_mail = message.sent_to[0]['email']

			# If html body is empty, load the plain
			if sanitized_body == "[]":
				sanitized_body = message.body['plain']

			if uid.decode() in unread_uid:
				unread = False
			else:
				unread = True

			Subject = str(message.subject) if str(message.subject) else "(No subject)"
			appmails = {
				'uid': uid.decode(),
				'From_name': str(From_name),
				'From_mail': str(From_mail),
				'To_name': str(To_name),
				'To_mail': str(To_mail),
				'Subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': str(datetime.date(year,month,day)),
				'readed': unread
				}
			mails.append(appmails)

			"""db_api.insert("emails",
				{
				'uid': uid.decode(),
				'from_name': str(From_name),
				'from_mail': str(From_mail),
				'to_name': str(To_name),
				'to_mail': str(To_mail),
				'subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': datetime.date(year,month,day)
				})"""
		return mails

@eel.expose
def mark_as_seen(uid):
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:
		imbox.mark_seen(uid)

@eel.expose
def get_number_unread():
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

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
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x
		all_inbox_messages = imbox.messages(unread=True)
		unread_msgs = imbox.messages(unread=True)
		unread_uid = []
		for uid, msg in unread_msgs:
			unread_uid.append(uid.decode())
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
			if sanitized_body == "[]":
				sanitized_body = str(message.body['plain'])
			sanitized_body = sanitized_body.replace(r"['\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"[b'", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r", "&#13;")
			sanitized_body = sanitized_body.replace(r"\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\t", "")
			sanitized_body = sanitized_body.replace(r"['", "")
			sanitized_body = sanitized_body.replace(r"']", "")

			# Apply local time to base server time
			From_name = message.sent_from[0]['name']
			From_mail = message.sent_from[0]['email']
			To_name = message.sent_to[0]['name']
			To_mail = message.sent_to[0]['email']

			# If html body is empty, load the plain
			if sanitized_body == "[]":
				sanitized_body = message.body['plain']

			if uid.decode() in unread_uid:
				unread = False
			else:
				unread = True

			Subject = str(message.subject) if str(message.subject) else "(No subject)"
			appmails = {
				'uid': uid.decode(),
				'From_name': str(From_name),
				'From_mail': str(From_mail),
				'To_name': str(To_name),
				'To_mail': str(To_mail),
				'Subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': str(message.date),
				'readed': unread
				}
			mails.append(appmails)

			"""db_api.insert("emails",
				{
				'uid': uid.decode(),
				'from_name': str(From_name),
				'from_mail': str(From_mail),
				'to_name': str(To_name),
				'to_mail': str(To_mail),
				'subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': datetime.date(year,month,day)
				})"""
		return mails

@eel.expose
def get_starred():
	mails = []
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x
		all_inbox_messages = imbox.messages(flagged=True)
		unread_msgs = imbox.messages(unread=True)
		unread_uid = []
		for uid, msg in unread_msgs:
			unread_uid.append(uid.decode())
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
			if sanitized_body == "[]":
				sanitized_body = str(message.body['plain'])
			sanitized_body = sanitized_body.replace(r"['\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"[b'", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r", "&#13;")
			sanitized_body = sanitized_body.replace(r"\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\t", "")
			sanitized_body = sanitized_body.replace(r"['", "")
			sanitized_body = sanitized_body.replace(r"']", "")

			# Apply local time to base server time
			From_name = message.sent_from[0]['name']
			From_mail = message.sent_from[0]['email']
			To_name = message.sent_to[0]['name']
			To_mail = message.sent_to[0]['email']

			# If html body is empty, load the plain
			if sanitized_body == "[]":
				sanitized_body = message.body['plain']

			if uid.decode() in unread_uid:
				unread = False
			else:
				unread = True

			Subject = str(message.subject) if str(message.subject) else "(No subject)"
			appmails = {
				'uid': uid.decode(),
				'From_name': str(From_name),
				'From_mail': str(From_mail),
				'To_name': str(To_name),
				'To_mail': str(To_mail),
				'Subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': str(message.date),
				'readed': unread
				}
			mails.append(appmails)

			"""db_api.insert("emails",
				{
				'uid': uid.decode(),
				'from_name': str(From_name),
				'from_mail': str(From_mail),
				'to_name': str(To_name),
				'to_mail': str(To_mail),
				'subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': datetime.date(year,month,day)
				})"""
		return mails

@eel.expose
def get_sent():
	mails = []
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x
		all_inbox_messages = imbox.messages(sent_from=username)
		unread_msgs = imbox.messages(unread=True)
		unread_uid = []
		for uid, msg in unread_msgs:
			unread_uid.append(uid.decode())
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
			if sanitized_body == "[]":
				sanitized_body = str(message.body['plain'])
			sanitized_body = sanitized_body.replace(r"['\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"[b'", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r", "&#13;")
			sanitized_body = sanitized_body.replace(r"\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\t", "")
			sanitized_body = sanitized_body.replace(r"['", "")
			sanitized_body = sanitized_body.replace(r"']", "")

			# Apply local time to base server time
			From_name = message.sent_from[0]['name']
			From_mail = message.sent_from[0]['email']
			To_name = message.sent_to[0]['name']
			To_mail = message.sent_to[0]['email']

			# If html body is empty, load the plain
			if sanitized_body == "[]":
				sanitized_body = message.body['plain']

			if uid.decode() in unread_uid:
				unread = False
			else:
				unread = True

			Subject = str(message.subject) if str(message.subject) else "(No subject)"
			appmails = {
				'uid': uid.decode(),
				'From_name': str(From_name),
				'From_mail': str(From_mail),
				'To_name': str(To_name),
				'To_mail': str(To_mail),
				'Subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': str(message.date),
				'readed': unread
				}
			mails.append(appmails)

			"""db_api.insert("emails",
				{
				'uid': uid.decode(),
				'from_name': str(From_name),
				'from_mail': str(From_mail),
				'to_name': str(To_name),
				'to_mail': str(To_mail),
				'subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': datetime.date(year,month,day)
				})"""
		return mails

@eel.expose
def get_unwanted():
	mails = []
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x
		all_inbox_messages = imbox.messages(folder='Junk')
		unread_msgs = imbox.messages(unread=True)
		unread_uid = []
		for uid, msg in unread_msgs:
			unread_uid.append(uid.decode())
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
			if sanitized_body == "[]":
				sanitized_body = str(message.body['plain'])
			sanitized_body = sanitized_body.replace(r"['\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"[b'", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r", "&#13;")
			sanitized_body = sanitized_body.replace(r"\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\t", "")
			sanitized_body = sanitized_body.replace(r"['", "")
			sanitized_body = sanitized_body.replace(r"']", "")

			# Apply local time to base server time
			From_name = message.sent_from[0]['name']
			From_mail = message.sent_from[0]['email']
			To_name = message.sent_to[0]['name']
			To_mail = message.sent_to[0]['email']

			# If html body is empty, load the plain
			if sanitized_body == "[]":
				sanitized_body = message.body['plain']

			if uid.decode() in unread_uid:
				unread = False
			else:
				unread = True

			Subject = str(message.subject) if str(message.subject) else "(No subject)"
			appmails = {
				'uid': uid.decode(),
				'From_name': str(From_name),
				'From_mail': str(From_mail),
				'To_name': str(To_name),
				'To_mail': str(To_mail),
				'Subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': str(message.date),
				'readed': unread
				}
			mails.append(appmails)

			"""db_api.insert("emails",
				{
				'uid': uid.decode(),
				'from_name': str(From_name),
				'from_mail': str(From_mail),
				'to_name': str(To_name),
				'to_mail': str(To_mail),
				'subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': datetime.date(year,month,day)
				})"""
		return mails

@eel.expose
def get_deleted():
	mails = []
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x
		all_inbox_messages = imbox.messages(folder='Deleted')
		unread_msgs = imbox.messages(unread=True)
		unread_uid = []
		for uid, msg in unread_msgs:
			unread_uid.append(uid.decode())
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
			if sanitized_body == "[]":
				sanitized_body = str(message.body['plain'])
			sanitized_body = sanitized_body.replace(r"['\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"[b'", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r", "&#13;")
			sanitized_body = sanitized_body.replace(r"\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\t", "")
			sanitized_body = sanitized_body.replace(r"['", "")
			sanitized_body = sanitized_body.replace(r"']", "")

			# Apply local time to base server time
			From_name = message.sent_from[0]['name']
			From_mail = message.sent_from[0]['email']
			To_name = message.sent_to[0]['name']
			To_mail = message.sent_to[0]['email']

			# If html body is empty, load the plain
			if sanitized_body == "[]":
				sanitized_body = message.body['plain']

			if uid.decode() in unread_uid:
				unread = False
			else:
				unread = True

			Subject = str(message.subject) if str(message.subject) else "(No subject)"
			appmails = {
				'uid': uid.decode(),
				'From_name': str(From_name),
				'From_mail': str(From_mail),
				'To_name': str(To_name),
				'To_mail': str(To_mail),
				'Subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': str(message.date),
				'readed': unread
				}
			mails.append(appmails)

			"""db_api.insert("emails",
				{
				'uid': uid.decode(),
				'from_name': str(From_name),
				'from_mail': str(From_mail),
				'to_name': str(To_name),
				'to_mail': str(To_mail),
				'subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': datetime.date(year,month,day)
				})"""
		return mails


@eel.expose
def send_mail(account, to, subject, body, attach):
	pass

@eel.expose
def get_flagged():
	mails = []
	username = backend_api.get_user_info("mail")
	passw = backend_api.get_user_info("password")
	imapserver = backend_api.get_user_info("imapserver")
	with Imbox(imapserver,
        username=username,
        password=passw,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x
		all_inbox_messages = imbox.messages(flagged=True)
		unread_msgs = imbox.messages(unread=True)
		unread_uid = []
		for uid, msg in unread_msgs:
			unread_uid.append(uid.decode())
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
			if sanitized_body == "[]":
				sanitized_body = str(message.body['plain'])
			sanitized_body = sanitized_body.replace(r"['\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"[b'", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\r", "&#13;")
			sanitized_body = sanitized_body.replace(r"\n", "&#13;")
			sanitized_body = sanitized_body.replace(r"\t", "")
			sanitized_body = sanitized_body.replace(r"['", "")
			sanitized_body = sanitized_body.replace(r"']", "")

			# Apply local time to base server time
			From_name = message.sent_from[0]['name']
			From_mail = message.sent_from[0]['email']
			To_name = message.sent_to[0]['name']
			To_mail = message.sent_to[0]['email']

			# If html body is empty, load the plain
			if sanitized_body == "[]":
				sanitized_body = message.body['plain']

			if uid.decode() in unread_uid:
				unread = False
			else:
				unread = True

			Subject = str(message.subject) if str(message.subject) else "(No subject)"
			appmails = {
				'uid': uid.decode(),
				'From_name': str(From_name),
				'From_mail': str(From_mail),
				'To_name': str(To_name),
				'To_mail': str(To_mail),
				'Subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': str(datetime.date(year,month,day)),
				'readed': unread
				}
			mails.append(appmails)

			"""db_api.insert("emails",
				{
				'uid': uid.decode(),
				'from_name': str(From_name),
				'from_mail': str(From_mail),
				'to_name': str(To_name),
				'to_mail': str(To_mail),
				'subject': str(Subject),
				'bodyHTML': str(sanitized_body),
				'bodyPLAIN': str(message.body['plain']),
				'directory': "",
				'datetimes': datetime.date(year,month,day)
				})"""
		return mails

@eel.expose
def delete_mail(uid):
	db_api.delete("mails",uid)
	backend_api.update_mails()

@eel.expose
def add_note(text,uid,attach):
	db_api.insert("notes",
		{
		'uid': uid,
		'attach': attach
		})

@eel.expose
def del_note(uid):
	db_api.delete("notes",uid)

@eel.expose
def add_contact(name,surname,mail,note,nick):
	db_api.insert("contact",
		{
		'name': name,
		'surname': surname,
		'mail': mail,
		'note': note,
		'nick': nick
		})
	

@eel.expose
def get_contacts():
	pass

@eel.expose
def event():
	# notify the frontend for incoming events
	pass

@eel.expose
def other():
	pass

@eel.expose
def set_user(name,nick,mail,passw,imapserver):
	db_api.insert("user",
		{
		'name': name,
		'surname': "",
		'nickname': nick,
		'bio': "",
		'mail': mail,
		'password': passw,
		'profilepic': "",
		'imapserver': imapserver,
		'smtpserver': "",
		'datetime': datetime.datetime.now(),
		})

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

template = check_if_user_exists()

eel.start(template, mode='electron')    # Start

conn.close()