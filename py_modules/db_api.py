import sqlite3
import json

"""
DB Structure

--- USER
(id)	name surname nickname bio mail password profilepic imapserver smtpserver

--- NOTES
(id)	UID note datetime

--- CONTACTS
(id)	name surname nick mail note datetime

"""

### CREATE ALL THE TABLES
DB_LOCATION = ".db/app.db"

conn = sqlite3.connect(DB_LOCATION)
# c = conn.cursor()

conn = sqlite3.connect(DB_LOCATION)
c = conn.cursor()

# --- user table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS user (
 id integer PRIMARY KEY,
 name text NOT NULL,
 surname text,
 nickname text,
 bio text,
 mail text,
 password text,
 profilepic text,
 imapserver text,
 smtpserver text,
 is_logged_in text,
 mail_server_setting,
 datetime datetime
);"""
)
# commit the changes to db
conn.commit()

# --- mail_server_settings table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS mail_server_settings (
 id integer PRIMARY KEY,
 service_name text NOT NULL,
 server_smtp text,
 server_imap text,
 ssl text,
 ssl_context text,
 starttls text
);"""
)
# commit the changes to db
conn.commit()

# --- mail table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS mails (
 id integer PRIMARY KEY,
 uuid text NOT NULL,
 subject text,
 user_id text,
 datetime datetime
);"""
)
# commit the changes to db
conn.commit()

# --- notes table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS notes (
 id integer PRIMARY KEY,
 uid text NOT NULL,
 note text,
 files text,
 datetime datetime
);"""
)
# commit the changes to db
conn.commit()

# --- contacts table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS contacts (
 id integer PRIMARY KEY,
 name text NOT NULL,
 surname text,
 nick text,
 mail text NOT NULL,
 note text,
 datetime datetime
);"""
)
# commit the changes to db
conn.commit()

# --- files table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS files (
         id integer PRIMARY KEY,
         uuid text NOT NULL,
         subject text,
         real_filename text,
         saved_as text,
         user_id text,
         deleted text,
         datetime datetime
    );"""
)
# commit the changes to db
conn.commit()

# close the connection
# conn.close()

""" BASIC SQLITE FUNCTIONS """


def insert(table, data):
    cols = ", ".join('"{}"'.format(col) for col in data.keys())
    vals = ", ".join(":{}".format(col) for col in data.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, data)
    conn.commit()
    return True
    """example
	sqlite_insert(conn, 'stocks', {
		'created_at': '2016-04-17',
		'type': 'BUY',
		'amount': 500,
		'price': 45.00})
	"""


def update(table, where, data):
    return


def delete(table, where, what):
    cur = conn.cursor()
    cur.execute("DELETE FROM " + table + " WHERE " + where + " LIKE %" + what + "%")
    cur.commit()


def drop(table):
    cur = conn.cursor()
    cur.execute("DROP TABLE " + table + "")
    cur.commit()


def get(table, field, expressions):
    cur = conn.cursor()
    cur.execute("SELECT " + field + " FROM " + table + " " + expressions + "")

    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(row)

    return data


""" UPLOADING APP SETTINGS """
with open(".db/mail_server.json", "r") as f:
    datastore = json.load(f)

    for setting in datastore:
        insert("mail_server_settings", setting)
