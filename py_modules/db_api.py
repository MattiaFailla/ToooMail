import sqlite3
import json


class DBApi:
    def __init__(self, table=None):
        self.table = table
        self.DB_LOCATION = ".db/app.db"
        self.conn = sqlite3.connect(DB_LOCATION, detect_types=sqlite3.PARSE_DECLTYPES |
                                                              sqlite3.PARSE_COLNAMES)

    def insert(self, data):
        cols = ", ".join('"{}"'.format(col) for col in data.keys())
        vals = ", ".join(":{}".format(col) for col in data.keys())
        sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(self.table, cols, vals)
        self.conn.cursor().execute(sql, data)
        self.conn.commit()
        return True

    def delete(self, where, what):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM "{0}" WHERE "{1}" LIKE %"{2}"%'.format(self.table, where, what))
        self.conn.commit()
        return

    def get(self, field: object = "", expression: object = "") -> object:
        cur = self.conn.cursor()
        cur.execute("SELECT " + field + " FROM " + self.table + " " + expression + "")
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(row)

        return data

    def drop(self):
        return

    def update(self):
        return

    def get_last_email_id(self, user_id):
        cur = self.conn.cursor()
        cur.execute("SELECT uuid FROM mails WHERE user_id = " + str(user_id) + " ORDER BY uuid DESC LIMIT 1")
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(row)

        return data

    def get_mail(self, step=None, user_id=0, folder="Inbox"):
        if step is not None:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT * FROM mails WHERE user_id = " + str(user_id) + " ORDER BY received DESC LIMIT 100")
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append(row)
            return data
        else:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT * FROM mails WHERE user_id = " + str(user_id) + " AND folder LIKE '%" + folder + "%' ORDER BY received DESC")
            rows = cur.fetchall()
            data = []
            for row in rows:
                data.append(row)
            return data

    @staticmethod
    def upload_config():
        """ UPLOADING APP SETTINGS """
        with open(".db/mail_server.json", "r") as f:
            datastore = json.load(f)

            for setting in datastore:
                DBApi("mail_server_settings").insert(setting)

    def get_next_uuid_set(self, uid, user_id, folder):
        cur = self.conn.cursor()
        cur.execute("SELECT uuid FROM mails WHERE uuid > " + str(uid) + " AND user_id = " + str(
            user_id) + " AND folder = '" + folder + "' ORDER BY uuid LIMIT 30")
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(row)
        return data

    def get_files_information(self, uid, user_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT real_filename, deleted FROM files WHERE uuid = " + str(uid) + " AND user_id = " + str(user_id) + "")
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append(row)
        return data

    def mark_as_seen(self, uid):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE mails SET opened = 1 WHERE uuid = " + str(uid) + "")
        self.conn.commit()

    def get_unopened(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM mails WHERE opened = 0")
        (number_of_rows,) = cur.fetchone()
        return number_of_rows


### CREATE ALL THE TABLES

DB_LOCATION = ".db/app.db"
conn = sqlite3.connect(DB_LOCATION)
c = conn.cursor()

queries = {"create_table":
               """CREATE TABLE IF NOT EXISTS user (
            id integer PRIMARY KEY, -- unique user id
            name text NOT NULL, -- user name
            surname text, -- user surname (optional)
            nickname text, -- user nickname (optional)
            bio text, -- user bio (optional)
            mail text, -- user email address
            password text, -- user email password
            app_password text, -- app password to unlock (optional)
            profilepic text, -- user profile pic ((optional), must contain the local file reference)
            imapserver text, -- imap server address
            smtpserver text, -- smtp server address
            is_logged_in integer, -- flag to check if the user is logged in the app
            mail_server_setting, -- external id (mail_server_settings)
            datetime datetime -- datetime of the user registration
           );""",

           "mail_server_settings":
               """CREATE TABLE IF NOT EXISTS mail_server_settings (
            id integer PRIMARY KEY, -- unique setting entry id
            service_name text NOT NULL, -- display name of the service
            server_smtp text, -- smtp server address
            server_imap text, -- imap server address 
            ssl text, -- ssl setting
            ssl_context text, -- ssl_context setting
            starttls text -- starttls setting
           );""",
           "emails_table":
               """CREATE TABLE IF NOT EXISTS mails (
            id integer PRIMARY KEY, -- the entry id
            uuid text NOT NULL, -- the mail uuid
            subject text, -- the mail subject
            user_id text, -- the user id
            folder text, -- the folder name
            opened integer, -- flag to check if email has been opened
            received text -- datetime from the imap server
           );""",
           "notes_table":
               """CREATE TABLE IF NOT EXISTS notes (
            id integer PRIMARY KEY, -- the note entry id
            uuid text NOT NULL, -- the mail uuid
            note text, -- the note body
            files text, -- attached file, must contain fs reference
            saved text -- datetime of the last saved note
           );""",
           "contacts_table":
               """CREATE TABLE IF NOT EXISTS contacts (
            id integer PRIMARY KEY,
            name text NOT NULL,
            surname text,
            nick text,
            mail text NOT NULL,
            note text,
            added text
           );""",
           "files_table":
               """CREATE TABLE IF NOT EXISTS files (
                    id integer PRIMARY KEY,
                    uuid text NOT NULL, -- the mail uuid
                    subject text, -- the mail subject (redundant)
                    real_filename text, -- real filename 
                    saved_as text, -- filename in the local fs
                    user_id text, -- the user id (owner of the file)
                    deleted text, -- flag to indicate if the file has been gracefully deleted
                    added text -- datetime from server
               );"""
           }

# execute queries
for query in queries.items():
    c.execute(query[1])

# saves result
conn.commit()
