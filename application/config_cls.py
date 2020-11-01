"""Provides congifuration class.

    List of classes:
        Config
    """
import ast
import os
from sys import platform
import configparser
from coin_cls import Coin


class Config:
    """Configuration class to keep default values in a file.

    Attr:
        __config (object) = python configparser object
    """

    __config = configparser.ConfigParser()

    def __init__(self, exc_list):
        """Constructor of config class.
        """

        self.__check_config_file()
        self.__config.read('config.ini')
        # self.__set_exc_coins(exc_list)

    @property
    def platform(self):
        """Provides the current operating system.

        Returns:
            [str]: current operating system
        """
        return platform

    @property
    def save_path(cls):
        """Provides the default save folder path.

        Returns:
            [str]: path of default save folder
        """
        return cls.__config['SYSTEM']['SaveFolder']

    @property
    def start_date(cls):
        """Provides default start date.

        Returns:
            [str]: default start date
        """
        return cls.__config['SYSTEM']['StartDate']

    @property
    def start_hour(cls):
        """Provides default start hour.

        Returns:
            [str]: default start hour
        """
        return cls.__config['SYSTEM']['StartHour']

    @classmethod
    def __check_config_file(cls):
        """Checks and creates if config.ini file does not exist.
        """
        path = os.getcwd()
        file = os.path.join(path, 'config.ini')
        if not os.path.isfile(file):
            cls.__create_config_file()

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
    def change_save_path(cls, new_path):
        """Changes save folder path and saves it into config.ini file.

        Args:
            new_path (str): new save folder path

        Raises:
            NotADirectoryError: new path does not exist
        """
        if not os.path.isdir(new_path):
            raise NotADirectoryError(
                f'{new_path} is not a valid directory!'
            )
        else:
            cls.__config['SYSTEM']['SaveFolder'] = new_path
            cls.__write_config_file()

    @classmethod
    def __write_config_file(cls):
        """Save __config obj to config.ini
        """
        with open('config.ini', 'w') as file:
            cls.__config.write(file)

    @classmethod
    def update_config_file(cls, exc):
        """Updates exchange and coins data in config.ini file.

        Args:
            exc_name (str): Name of exchange
        """
        data = {coin.name: [coin.abbr,
                            coin.start_date,
                            coin.start_hour,
                            coin.end_date,
                            coin.end_hour] for coin in exc.coins}
        cls.__config[exc.name] = data
        cls.__write_config_file()

    @classmethod
    def set_coins_of_exchange(cls, exc):
        """Reads coins from config.ini and adds to exchanges' coin list.

        Args:
            exc (obj): exchange 
        """
        for coin in exc.coins:
            exc.abandon_coin(coin)
        if exc.name in cls.__config:
            for coin in cls.__config[exc.name]:
                coin_data = cls.__get_coin_data(exc, coin)
                exc.possess_coin(Coin(exc, coin_data))

    @classmethod
    def __get_coin_data(cls, exc, coin):
        """Reads coin data from config ini

        Args:
            exc (obj): exchange possesing coin
            coin (obj): target coin

        Returns:
            dict: data of target coin
        """
        data = ast.literal_eval(cls.__config[exc.name][coin])
        return {'Name': coin,
                'Abbr': data[0],
                'StartDate': data[1],
                'StartHour': data[2],
                'EndDate': data[3],
                'EndHour': data[4]}
