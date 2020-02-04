import json
import logging.config
import os

__file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(__file_dir, 'logging.ini'), disable_existing_loggers=False)


class Configuration:
    """
    This class represents the current configuration of the whole app.
    Any configuration parameter can and should be retrieved through an instance of this class.
    """

    def __init__(self):
        file_dir = os.path.split(os.path.realpath(__file__))[0]
        with open(os.path.join(file_dir, 'config.json'), 'r') as config_file, \
                open(os.path.join(file_dir, 'mail_server.json'), 'r') as mail_server_file:
            parsed_file = json.loads(config_file.read())
            self.__db_location = parsed_file['db_location']
            self.__migrations_location = parsed_file['db_migrations_location']
            self.__logger = logging.getLogger('root')
            self.__mail_server_settings = [setting for setting in json.load(mail_server_file)]

    @property
    def db_location(self):
        """
        Getter for the db location path
        :return: a str representing the db location
        """
        return self.__db_location

    @property
    def migrations_location(self):
        """
        Getter for the migrations folder location
        :return: a str representing the migrations folder location
        """
        return self.__migrations_location

    @property
    def mail_server_settings(self):
        """
        Getter for the mail server settings
        :return: a dict with the loaded mail server settings.
        """
        return self.__mail_server_settings

    @property
    def logger(self):
        """
        Getter for the configured logger
        :return: a logger
        """
        return self.__logger


__current_configuration = Configuration()


def get_current():
    return __current_configuration
