import os
import platform
import shutil
import sqlite3
import subprocess
from pathlib import Path

import configuration

current_configuration = configuration.get_current()
logger = current_configuration.logger


class TagApi:

    db_location = Path(current_configuration.db_location)

    def __init__(self, user_id):
        """Constructor method for TagApi class

        :param user_id: The email account identification number used in sqlite database
        :type user_id: int
        """
        self.user_id = user_id

    def get_tags(self):
        conn = sqlite3.connect(current_configuration.db_location)
        c = conn.cursor()
        c.execute("SELECT id, name, color FROM tags WHERE user_id = ?;", (self.user_id,))
        rows = c.fetchall()

        tags = []
        keys = ["id", "name", "color"]
        for f in rows:
            tags.append({keys[j]: f[j] for j in range(3)})

        conn.close()
        return tags

    def create_tag(self, tag_name, color):
        conn = sqlite3.connect(current_configuration.db_location)
        c = conn.cursor()
        c.execute("INSERT INTO tags (name, user_id, color) VALUES (?, ?, ?);", (tag_name, self.user_id, color))
        conn.commit()
        tag_id = c.lastrowid
        conn.close()
        return tag_id


    def set_tag(self, uuid, tag_name):
        # todo
        pass



        