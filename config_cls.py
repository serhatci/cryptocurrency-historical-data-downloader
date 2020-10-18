"""Provides congifuration class.

    List of classes:
        Config
    """
import ast
import os
from sys import platform
import configparser


class Config:
    """Configuration class to keep default values in a file.

    Attr:
        __config (object) = python configparser object
    """

    __config = configparser.ConfigParser()

    def __init__(self, exc_list):
        """Constructor of config class.
        """

        self.__config_file_check()
        self.__config.read('config.ini')
        self.__set_exc_coins(exc_list)

    @property
    def platform(self):
        """Gets the current operating system.

        Returns:
            [str]: current operating system
        """
        return platform

    @property
    def folder_path(cls):
        """Gets the default save folder path.

        Returns:
            [str]: path of default save folder
        """
        return cls.__config['SYSTEM']['SaveFolder']

    @property
    def start_date(cls):
        """Gets default start date.

        Returns:
            [str]: default start date
        """
        return cls.__config['SYSTEM']['StartDate']

    @property
    def start_hour(cls):
        """Gets default start hour.

        Returns:
            [str]: default start hour
        """
        return cls.__config['SYSTEM']['StartHour']

    @classmethod
    def __config_file_check(cls):
        """Checks and creates config.ini file if not exists.
        """
        if not os.path.isfile('config.ini'):
            cls.__create_config_file()

    @classmethod
    def __create_config_file(cls):
        """Creates config.ini file with default values.
        """
        cls.__config['SYSTEM'] = {'Platform': platform,
                                  'SaveFolder': os.getcwd(),
                                  'StartDate': '01-01-2020',
                                  'StartHour': '00:00:00'}
        cls.__write_config_file()

    @classmethod
    def change_folder_path(cls, path):
        """Changes save folder path and save into config.ini

        Args:
            path (str): New folder path
        """
        cls.__config['SYSTEM']['SaveFolder'] = path
        cls.__write_config_file()

    @classmethod
    def __write_config_file(cls):
        """Save __config obj to config.ini
        """
        with open('config.ini', 'w') as configfile:
            cls.__config.write(configfile)

    @classmethod
    def save_coins(cls, exc_name, coins):
        cls.__config[exc_name] = coins
        cls.__write_config_file()

    @classmethod
    def __set_exc_coins(cls, exchanges):
        for exc in exchanges:
            if exc.name in cls.__config:
                for coin in cls.__config[exc.name]:
                    data = ast.literal_eval(
                        cls.__config[exc.name][coin]
                    )
                    exc.set_coins('+', coin, data)
