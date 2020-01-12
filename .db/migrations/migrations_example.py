import sqlite3
import os
import re
import hashlib
import importlib
from datetime import datetime

MIGRATION_FILE_PATTERN = r'([0-9]{4}-([0][0-9](?=)|[1][0-2])-([0,1,2][0-9](?=)|[3][0,1]))-([0-9]+)_([a-zA-Z0-9_-]+)\.py'

if __name__ == "__main__":
    connection = sqlite3.connect('./db/app.db')
    connection.execute('create table if not exists migrations(' \
                       'id integer primary key,' \
                       'date_string text,' \
                       'date_millis integer,' \
                       'progressive_number integer,' \
                       'file_name text,' \
                       'checksum text);')
    directory = os.listdir('./db/migrations')
    for file_name in directory:
        result = re.search(MIGRATION_FILE_PATTERN, file_name)
        if result:
            migration_date, progressive_number, migration_name = result.group(1), result.group(4), result.group(5)
            checksum = hashlib.md5(migration_name.encode()).hexdigest()
            module = importlib.import_module('db.migrations.' + file_name.replace('.py', ''))
            connection.execute(module.update())
            date_millis = (datetime.strptime(migration_date, "%Y-%m-%d") - datetime.utcfromtimestamp(0)).total_seconds()
            query = f"insert into migrations values ( ( select coalesce(max(id), 0)+1 from migrations ), '{migration_date}', {int(date_millis)}, {progressive_number}, '{migration_name}', '{checksum}');"
            connection.execute(query)
            connection.commit()



