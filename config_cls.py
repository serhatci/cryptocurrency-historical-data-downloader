import os
from sys import platform
import configparser


class Config:

    __config = configparser.ConfigParser()

    def __init__(self):

        self.__config_file_check()
        self.__config.read('config.ini')
        self.platform = platform
        self.folder_path = self.__config['DEFAULT']['SaveFolder']

    @classmethod
    def __config_file_check(cls):
        if not os.path.isfile('config.ini'):
            cls.__create_config_file()

    @classmethod
    def __create_config_file(cls):
        cls.__config['DEFAULT'] = {'Platform': platform,
                                   'SaveFolder': os.getcwd()}
        cls.__write_config_file()

    @classmethod
    def change_folder_path(cls, path):
        cls.__config['DEFAULT']['SaveFolder'] = path
        cls.__write_config_file()

    @classmethod
    def __write_config_file(cls):
        with open('config.ini', 'w') as configfile:
            cls.__config.write(configfile)
