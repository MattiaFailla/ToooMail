import threading
from imbox import Imbox
# from pynotifier import Notification

# DOWNLOAD WITH LAST DATE

def get_user_connection_data():
	data = ['imap-mail.outlook.com',
			'mattiafailla@hotmail.it',
			'pass',
			True,
			None,
			False]
	return data

def get_mails(year, month, day):

	# Messages received after specific date
    #inbox_messages_received_after = imbox.messages(date__gt=datetime.date(2018, 7, 30))
	
	mails = []
	with Imbox(get_user_connection_data()) as imbox:

		logging.info('Account informations correct. Connected.')

		# Gets all messages after the day x

		# to get the mails of today:
		all_inbox_messages = imbox.messages(date__on=datetime.date(year,month,day))
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
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

			Subject = str(message.subject) if str(message.subject) else "(No subject)"

			db_api.insert("emails",
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
				})

def test_user_connection_data(imap, username,password):
	try:
		Imbox(imap,username,password,True,None,False)
		return True
	except Exception as e:
		return False

def first_download():
	""" DOWNLOAD 200 MAILS FROM THE POSTAL 
		AND SAVE THEM IN THE DB

		Run only on the first login - When the 
		user scrolls down more emails are downloader
		from the server
	"""
	mails = []
	with Imbox(get_user_connection_data()) as imbox:

		logging.info('Account informations correct.')

		# Gets all messages from the inbox
		all_inbox_messages = imbox.messages()
		print(len(all_inbox_messages))
		logging.debug('Gathered all inbox messages')

		for uid, message in reversed(all_inbox_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
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

			Subject = str(message.subject) if str(message.subject) else "(No subject)"

			data = [uid.decode(),
			str(From_name),
			str(From_mail),
			str(To_name),
			str(To_mail),
			str(Subject),
			str(sanitized_body),
			str(message.body['plain']),
			'Inbox',
			str(message.date)
			]

			insert("emails",data)
			"""
			# INSERT INTO THE DB
			try:
				c.execute('INSERT INTO emails (uid, from_name, from_mail, to_name, to_mail, subject, bodyHTML, bodyPLAIN, directory, datetimes) VALUES (?,?,?,?,?,?,?,?,)', data)
			except sqlite3.IntegrityError as e:
				print('sqlite error: ', e) # column name is not unique
				continue
			conn.commit()"""

def notify(title,description,duration):
	Notification(
		title=title,
		description=description,
		icon_path='favicon.ico', # On Windows .ico is required, on Linux - .png
		duration=duration,                              # Duration in seconds
		urgency=Notification.URGENCY_CRITICAL
	).send()

def elaborate_new_mails(new_messages):
	# NEW MAILS! Add them to the db, send notification and notify the frontend
	for uid, message in reversed(new_messages):
			#print(message.attachments)
			sanitized_body = str(message.body['html'])
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

			Subject = str(message.subject) if str(message.subject) else "(No subject)"

			data = [uid.decode(),
			str(From_name),
			str(From_mail),
			str(To_name),
			str(To_mail),
			str(Subject),
			str(sanitized_body),
			str(message.body['plain']),
			'Inbox',
			str(message.date)
			]

			insert("emails",data)

	numer_of_new_mails = len(new_messages)

	# Notify the frontend
	notify_frontend("new_messages")




def check_for_incoming_mails():
	threading.Timer(5.0, download_new_emails).start() # check every five seconds
	""" CONNECT TO THE ACCOUNT AND THEN DOWNLOAD THE WHOLE MAIL """
	with Imbox(get_user_connection_data()) as imbox:
		# get the last mail UID
		last_uid = get("last_uid","uid","")
		# Messages whose UID is greater than last_uid
		last_messages = imbox.messages(uid__range=''+int(last_uid)+':*')

		if last_messages:
			elaborate_new_mails(last_messages)

