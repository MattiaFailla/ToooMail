import sqlite3
import json
import os
import re
import hashlib
import importlib.util
from datetime import datetime


class MigrationException(Exception):
    """
    This exception represents a generic error in the execution of the code of a migration.
    """
    pass


class NotAMigrationException(MigrationException):
    """
    This exception is triggered any time a Migration class is built over a file that doesn't respect the naming
    convention for ToooMail migrations (yyyy-MM-dd-n-migrationName.py).
    """
    pass


class AlreadyMigratedException(MigrationException):
    """
    This exception is triggered when the system tries to execute a migration that has already been executed.
    """
    pass


class DifferentChecksumMigrationException(MigrationException):
    """
    This exception is triggered when the system finds a migration which name or content has been modified since its
    execution.
    """
    pass


class OldStateMigrationException(MigrationException):
    """
    This exception is triggered when the system finds a not executed migration that has a date older than the last
    executed migration.
    """
    pass


class DBApi:

    def __init__(self, table=None):
        self.table = table
        self.DB_LOCATION = ".db/app.db"
        self.conn = sqlite3.connect(DB_LOCATION, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    def __del__(self):
        self.conn.close()

    def insert(self, data):
        columns = ", ".join('"{}"'.format(col) for col in data.keys())
        values = ", ".join(":{}".format(col) for col in data.keys())
        sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(self.table, columns, values)
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
        """
        TODO Implement drop method.
        :return:
        """
        pass

    def update(self):
        """
        TODO Implement update method.
        :return:
        """
        pass

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
                "SELECT * FROM mails WHERE user_id = " + str(
                    user_id) + " AND folder LIKE '%" + folder + "%' ORDER BY received DESC")
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


class Migration:
    def __init__(self, file_name):
        self.file_name = file_name
        regex_result = re.search(MIGRATION_FILE_PATTERN, file_name)
        if regex_result:
            self.date_string = regex_result.group(1)
            self.progressive_number = regex_result.group(4)
            self.name = regex_result.group(5)
            self.date_millis = int((datetime.strptime(self.date_string, "%Y-%m-%d") -
                                    datetime.utcfromtimestamp(0)).total_seconds())
            spec = importlib.util.spec_from_file_location(file_name.replace('.py', ''),
                                                          MIGRATIONS_LOCATION+'/'+file_name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.sql_script = module.update()
            self.checksum = hashlib.md5((self.file_name+self.sql_script).encode()).hexdigest()
        else:
            raise NotAMigrationException('The given name does not represent a valid migration')

    def compare_to(self, other):
        if self.date_millis - other.date_millis != 0:
            return self.date_millis - other.date_millis
        elif self.progressive_number - other.progressive_number != 0:
            return self.progressive_number - other.progressive_number
        else:
            raise MigrationException("There are two migrations with same date and progressive number")


def validate_migration_execution(current_migration, current_connection):
    current_query = "select * from migrations where date_string = ? and progressive_number = ? limit 1"
    cursor = current_connection.execute(current_query,
                                        (current_migration.date_string, current_migration.progressive_number))
    value = cursor.fetchone()
    if value:
        if value[5] != current_migration.checksum:
            exception_message = f'The migration {current_migration.file_name} has been executed with checksum ' \
                                f'{value[5]} but the value {current_migration.checksum} was found.'
            raise DifferentChecksumMigrationException(exception_message)
        else:
            raise AlreadyMigratedException(f'The migration {current_migration.file_name} has already been executed.')

    current_query = "select * from migrations where date_millis > ? order by date_millis limit 1"
    cursor = current_connection.execute(current_query, (current_migration.date_millis,))
    value = cursor.fetchone()
    if value:
        raise OldStateMigrationException(
            f'There current migration state ({value[2]}) is more recent than {current_migration.date_string}')


def get_sorted_migrations(current_directory):
    migrations = []
    for file_name in current_directory:
        try:
            migrations.append(Migration(file_name))
        except NotAMigrationException:
            pass
    migrations.sort(key=lambda x: (x.date_millis, x.progressive_number))
    return migrations


# EXECUTING MIGRATIONS
MIGRATION_FILE_PATTERN = r'([0-9]{4}-([0][0-9](?=)|[1][0-2])-([0,1,2][0-9](?=)|[3][0,1]))-([0-9]+)_([a-zA-Z0-9_-]+)\.py'
DB_LOCATION = ".db/app.db"
MIGRATIONS_LOCATION = './.db/migrations'
connection = sqlite3.connect(DB_LOCATION)
connection.execute('create table if not exists migrations('
                   'id integer primary key,'
                   'date_string text,'
                   'date_millis integer,'
                   'progressive_number integer,'
                   'file_name text,'
                   'checksum text);')
connection.commit()
directory = os.listdir(MIGRATIONS_LOCATION)
migrations_list = get_sorted_migrations(directory)
for migration in migrations_list:
    try:
        validate_migration_execution(migration, connection)
        connection.executescript(migration.sql_script)

        query = 'insert into migrations values ( ( select coalesce(max(id), 0)+1 from migrations ), ?, ?, ?, ?, ?);'
        connection.execute(query, (migration.date_string, migration.date_millis, migration.progressive_number,
                                   migration.name, migration.checksum))
    except AlreadyMigratedException:
        pass

connection.commit()
connection.close()

""" UPLOADING APP SETTINGS """
with open(".db/mail_server.json", "r") as file:
    for setting in json.load(file):
        api = DBApi("mail_server_settings")
        result = [existing[1] for existing in api.get('*')]
        # , f'where service_name like \'{setting["service_name"]}\'')
        if not (setting['service_name'] in result):
            api.insert(setting)
