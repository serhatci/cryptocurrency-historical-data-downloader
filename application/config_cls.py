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

        self.__create_config_file()
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
    def __create_config_file(cls):
        f"""Creates and/or writes config.ini file with default values.
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
        with open('config.ini', 'w') as file:
            cls.__config.write(file)

    @classmethod
    def save_coins(cls, exc_name, coins):
        """Saves coins of an exchange to config.ini file.

        Args:
            exc_name (str): Name of exchange
            coins (list): List of coin objects
        """
        data = {coin.name: coin.data for coin in coins}
        cls.__config[exc_name] = data
        cls.__write_config_file()

    @ classmethod
    def __set_exc_coins(cls, exchanges):
        """Binds coin objects to relevant exchange object.

        Args:
            exchanges (list): List of exchange objects
        """
        for exc in exchanges:
            if exc.name in cls.__config:
                for coin in cls.__config[exc.name]:
                    # Converts string to dict
                    data = ast.literal_eval(
                        cls.__config[exc.name][coin]
                    )
                    exc.possess_coin(coin, data)
