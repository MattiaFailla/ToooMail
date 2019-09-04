import sqlite3

"""
Struttura db
--- EMAILS
(uid)	from to subject bodyHTML bodyPLAIN datetime starred directory
																|-> spam, deleted, starred, foldername

--- UNREADS
(id)	uid

--- SENT
(id)	to subject body attach datetime
		 |-> it may be a tuple

--- USER
(id)	name surname nickname bio mail password profilepic imapserver smtpserver

--- NOTES
(id)	UID note datetime

--- CONTACTS
(id)	name surname nick mail note datetime

--- LIST OF UIDS -> extract from the EMAILS table
--- NUMBER OF UNREAD -> count the number of entry in UNREADS table
--- LAST UID

Api
---- DOWNLOAD NEW MAILS

---- READ A MAIL

---- SEND AN EMAIL
---- DELETE A MAIL
---- STAR A MAIL

---- ANSWER A MAIL

---- SAVE A CONTACT
---- DELETE A CONTACT

---- ADD A USER
---- DELETE A USER

---- SAVE A NOTE
---- DELETE A NOTE
"""

### CREATE ALL THE TABLES
DB_LOCATION = "db/app.db"

conn = sqlite3.connect(DB_LOCATION)
# c = conn.cursor()

conn = sqlite3.connect(DB_LOCATION)
c = conn.cursor()

# --- emails table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS emails (
 uid integer PRIMARY KEY,
 from_name text NOT NULL,
 from_mail text NOT NULL,
 to_name text NOT NULL,
 to_mail text,
 subject text,
 bodyHTML text,
 bodyPLAIN text,
 directory text,
 datetimes datetime);"""
)
# commit the changes to db
conn.commit()


# --- unreads table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS unreads (
 id integer PRIMARY KEY,
 uid int NOT NULL);"""
)
# commit the changes to db
conn.commit()


# --- sent table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS sent (
 id integer PRIMARY KEY,
 to_mail text NOT NULL,
 subject text,
 body text,
 attach text,
 datetimes datetime);"""
)
# commit the changes to db
conn.commit()


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


# --- emails table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS last_uid (
 uid integer PRIMARY KEY);"""
)
# commit the changes to db
conn.commit()


# --- emails table
# create table
c.execute(
    """CREATE TABLE IF NOT EXISTS starred (
 uid integer PRIMARY KEY);"""
)
# commit the changes to db
conn.commit()
"""
FIRST RUN
Registration -> download of the whole postal -> save on the db

OTHER RUN
Check for new mails -> send in-app notification -> save in the db -> notify the frontend 
"""


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
    pass


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