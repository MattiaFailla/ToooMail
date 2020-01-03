import sqlite3
import json


class DBApi:
    def __init__(self, table):
        self.table = table
        self.DB_LOCATION = ".db/app.db"
        self.conn = sqlite3.connect(DB_LOCATION)

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


### CREATE ALL THE TABLES

DB_LOCATION = ".db/app.db"
conn = sqlite3.connect(DB_LOCATION)
c = conn.cursor()

queries = {"create_table":
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
            is_logged_in integer,
            mail_server_setting,
            datetime datetime
           );""",

           "mail_server_settings":
               """CREATE TABLE IF NOT EXISTS mail_server_settings (
            id integer PRIMARY KEY,
            service_name text NOT NULL,
            server_smtp text,
            server_imap text,
            ssl text,
            ssl_context text,
            starttls text
           );""",
           "emails_table":
               """CREATE TABLE IF NOT EXISTS mails (
            id integer PRIMARY KEY,
            uuid text NOT NULL,
            subject text,
            user_id text,
            datetime datetime
           );""",
           "notes_table":
               """CREATE TABLE IF NOT EXISTS notes (
            id integer PRIMARY KEY,
            uid text NOT NULL,
            note text,
            files text,
            datetime datetime
           );""",
           "contacts_table":
               """CREATE TABLE IF NOT EXISTS contacts (
            id integer PRIMARY KEY,
            name text NOT NULL,
            surname text,
            nick text,
            mail text NOT NULL,
            note text,
            datetime datetime
           );""",
           "files_table":
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
           }

# execute queries
for query in queries.items():
    c.execute(query[1])

# saves result
conn.commit()

""" UPLOADING APP SETTINGS """
with open(".db/mail_server.json", "r") as f:
    datastore = json.load(f)

    for setting in datastore:
        DBApi("mail_server_settings").insert(setting)
