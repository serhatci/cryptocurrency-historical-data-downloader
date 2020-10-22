import os
from config_cls import Config
import pandas as pd
import PySimpleGUI as sg  # GUI framework library
from exchange_base_cls import Exchange
from exchange_classes import *
from screen_layout import Layout


class Controller():
    """Provides controller object of MVC design.
    """

    def __init__(self):
        """Constructor of Controller class.

        Attr:
            model (object): model of MVC design
            view (object): view of MVC design
            __slc_exc (obj): User clicked exchange at run-time
                                (Default to None)
            __slc_coin (obj): User clicked coin at run-time
                                (Default to None)
        """
        self.model = Model()
        self.view = View()
        self.__slc_exc = None
        self.__slc_coin = None

    def start(self):
        """Starts application and listen window.
        """

        # Creates screen layout
        layout = Layout.create(self.model.exc_list,
                               self.model.sys.folder_path,
                               self.model.sys.start_date,
                               self.model.sys.start_hour)

        # Initializes application window
        self.view.window = sg.Window('Crypto-exchanges Data Downloader',
                                     layout,
                                     size=(1000, 520),
                                     finalize=True)

        # Listens the window and collects user inputs
        while True:
            event, values = self.view.window.read()

            # Terminates app when user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break

            # Changes save folder
            if event == '-change_folder-':
                new_folder = sg.popup_get_folder(
                    'Select a folder to save downloaded data',
                    title='Browse Folder',
                    default_path=self.model.sys.folder_path
                )
                try:
                    self.model.sys.change_folder_path(new_folder)
                except FileNotFoundError as err:
                    self.view.display_err(err)
                except IOError as err:
                    self.view.display_err(err)
                else:
                    self.view.window['-folder-'].update(new_folder)
                    self.view.display(
                        self.model.msg('*Folder Change'),
                        'green')

            # Displays coins belong to the selected exchange
            # Displays exchange info when it is clicked
            if event == '-exchanges_table-':
                col_num = values['-exchanges_table-'][0]
                self.__slc_exc = self.model.exc_list[col_num]
                try:
                    self.model.check_coins(self.__slc_exc)
                except FileNotFoundError as err:
                    self.view.display_err(err)
                except Warning as wrn:
                    self.view.display_err(wrn)
                else:
                    msg = f'{self.__slc_exc.name}\n--------\n' \
                          f'{self.__slc_exc.website}\n--------\n'
                    self.view.display(msg, 'green')
                    self.view.update_coin_tbl(self.__slc_exc.display())

            # Assign selected coin to a variable
            if event == '-coins_table-':
                if not self.__slc_exc:
                    self.view.display_err(
                        self.model.msg('*Select Exchange'))
                else:
                    col_num = values['-coins_table-'][0]
                    if self.__slc_exc.coins:
                        self.__slc_coin = self.__slc_exc.coins[col_num]

            # User clicks -add- button and a new coin is added
            if event == '-add_coin-':
                if not self.__slc_exc:
                    self.view.display_err(
                        self.model.msg('*Select Exchange'))
                else:
                    if (values['-coin_name-'] == '' or
                            values['-abbr-'] == ''):
                        self.view.display_err(
                            self.model.msg('*Missing Info'))
                    else:
                        coin_name = values['-coin_name-']
                        abbr = values['-abbr-']
                        start_date = self.view.window['-start_date-'].get()
                        start_hour = self.view.window['-start_hour-'].get()
                        try:
                            self.model.add_coin(self.__slc_exc,
                                                coin_name,
                                                abbr,
                                                start_date,
                                                start_hour)
                        except FileExistsError as err:
                            self.view.display_err(err)
                        except IOError as err:
                            self.view.display_err(err)
                        else:
                            self.view.display(
                                self.model.msg('*Coin added'),
                                'green'
                            )
                            self.view.update_coin_tbl(
                                self.__slc_exc.display())

            # User clicks update button and data starts to download
            if event == '-update_coin-':
                if not self.__slc_coin:
                    self.view.display_err(
                        self.model.msg('*Select Coin'))
                else:
                    self.model.download_data(self.__slc_coin)
                    self.view.update_coin_tbl(self.__slc_exc.display())

            # User clicks update all button and all data starts to download
            if event == '-update_all-':
                for coin in self.__slc_exc.coins:
                    self.model.download_data(coin)
                self.view.update_coin_tbl(self.__slc_exc.display())

            # User clicks delete button and coin data is deleted
            if event == '-delete_coin-':
                if not self.__slc_coin:
                    self.view.display_err(
                        self.model.msg('*Select Coin'))
                else:
                    self.model.delete_coin(self.__slc_exc, self.__slc_coin)
                    self.view.update_coin_tbl(self.__slc_exc.display())

        self.view.window.close()


class Model:
    """Provides model object of MVC design.

    attr:
        __exc_list (list): list of exchange objects
        __sys (obj) : Object that stores configuration data
    """

    __exc_list = [cls() for cls in Exchange.__subclasses__()]
    __sys = Config(__exc_list)

    @ property
    def sys(cls):
        """Provides System configurations.

        Returns:
            [obj]: system configurations
        """
        return cls.__sys

    @ property
    def exc_list(cls):
        """Provides list of exchanges.

        Returns:
            list: list of exchange objects
        """
        return cls.__exc_list

    @ staticmethod
    def msg(msg):
        """Provides a message from pre-defined message class.

        Args:
            msg (str): Short description of message

        Returns:
            str: full message ready to be displayed
        """
        full_msg = PredefinedMessages._messages[msg] + '\n---------\n'
        return full_msg

    def create_folder(self, path):
        """Creates a directory in the system.

        Args:
            path (str): path where directory will be created
        """
        os.mkdir(path)

    def delete_folder(self, folder_name):
        """Deletes given exchange folder.

        Args:
            folder_name (str): name of folder
        """
        path = os.path.join(self.sys.folder_path, folder_name)
        if os.path.isdir(path):
            os.rmdir(path)

    def create_file(self, file_path, cols):
        """Creates cvs files for a given coin.

        Args:
            file_path (str): file of path being created
            cols (list): list of default column names
        """
        df = pd.DataFrame(columns=cols)
        df.to_csv(file_path, index=False, sep=';')

    def delete_file(self, exc_name, file_name):
        """Deletes a given coin file.

        Args:
            exc_name (str): name of exchange
            file_name (str): full name of csv file

        Returns:
            (bool): True if file is deleted and false for failure
        """
        path = os.path.join(self.sys.folder_path, exc_name)
        file_path = os.path.join(path, file_name)
        if self.check_file(file_path):
            os.remove(file_path)

    def check_coins(self, exc):
        """Compare configuration file and system files.

        Checks if coins stored in config.ini file still exist
        in the system when the an exchange is clicked. If there are
        miss,ng files, corrects data in config.ini file according
        to the system data.

        Args:
            exc (obj): object of exchange

        Raise:
            Warning (str): warning message about any change was made
        """
        if exc.coins:
            files = self.files_in_folder(exc.name)
            for coin in exc.coins:
                file_name = self.create_file_name(exc, coin)
                if not file_name in files:
                    exc.abandon_coin(coin)
                    self.sys.save_coins(exc.name, exc.coins)
                    raise Warning(
                        f'{file_name} could not be found in save folder'
                        'and was excluded!'
                    )

    @ staticmethod
    def create_file_name(exc, coin):
        return '{}_{}_{}.csv'.format(
            coin.name,
            exc.name,
            coin.data['StartDate']
        )

    def files_in_folder(self, exc_name):
        """Provides all coin files in a given folder.

        Args:
            exc_name (str): name of exchange

        Returns:
            (list): List of coin files in the folder
        """
        path = os.path.join(self.sys.folder_path, exc_name)
        if not self.check_dir(path):
            raise FileNotFoundError(
                f'{path} could not be found!...')
        else:
            return os.listdir(path)

    def check_dir(self, dir):
        """Checks if given path is an existing directory.

        Args:
            dir (str): path of directory

        Returns:
            [bool]: True if it exist false if opposite
        """
        return os.path.isdir(dir)

    def check_file(self, file):
        """Checks if given path is an existing file.

        Args:
            file (str): path of file

        Returns:
            [bool]: True if it exist false if opposite
        """
        return os.path.isfile(file)

    def add_coin(self, exc, coin_name,
                 abbr, start_date, start_hour):
        """Adds new coins to the exchange and saves its csv file.

        Args:
            exc (obj): selected exchange for coin addition
            coin_name (str): name of coin
            abbr (str): abbreviation of coin
            start_date (str): start date
            start_hour (str): start hour
        """
        folder_path = os.path.join(self.sys.folder_path, exc.name)
        if not self.check_dir(folder_path):
            self.create_folder(exc.name)
        columns = [i['Column Name'] for i in exc.db_columns]
        file_name = f'{coin_name}_{exc.name}_{start_date}.csv'
        file_path = os.path.join(folder_path, file_name)
        if not self.check_file(file_path):
            self.create_file(exc.name, file_name, columns)
            coin_data = {'Abbr.': abbr,
                         'StartDate': start_date,
                         'StartHour': start_hour,
                         'EndDate': '-',
                         'EndHour': '-'}
            exc.possess_coin(coin_name, coin_data)
            self.sys.save_coins(exc.name, exc.coins)
        else:
            raise FileExistsError(
                f'{coin_name} already exists in the save folder'
                f' with file name of {file_name}'
            )

    def delete_coin(self, exc, coin):
        """Removes the coin file from system and config.ini.

        Args:
            exc (obj): exchange object
            coin (obj): coin object
        """
        file_name = f'{coin.name}_{exc.name}_{coin.data["StartDate"]}.csv'
        if self.delete_file(exc.name, file_name):
            if not self.files_in_folder(exc.name):
                self.delete_folder(exc.name)
            exc.abandon_coin(coin)
            self.sys.save_coins(exc.name, exc.coins)


class View:
    """Provides view object of MVC design.

    attr:
        window (obj): Pysimplegui window object
    """

    def display(self, msg, color):
        """Displays messages at action panel on the screen.

        Args:
            msg (str): desired message to be displayed
            color (str): desired color of the message
        """
        self.window['-output_panel-'].update(msg,
                                             text_color=color, append=False)

    def display_err(self, msg):
        """Displays error messages at action panel on the screen.

        Args:
            msg (str): desired message to be displayed
        """
        self.window['-output_panel-'].update(msg,
                                             text_color='red',
                                             append=True)
        self.window['-output_panel-'].update('\n---------\n',
                                             text_color='red',
                                             append=True)

    def update_coin_tbl(self, data):
        """Updates coins table in the screen.

        Args:
            data (dict): dict of coins will be displayed
        """
        self.window['-coins_table-'].update(data)


class PredefinedMessages:
    """Contains pre-defined messages to select display.

    Class Attr:
        __messages [dict]: dictionary of pre-defined messages
                         which users can select among them
    """
    _messages = {
        '*Select Exchange':
            'Please select an exchange first!..',
        '*Select Coin':
            'Please select a coin first!..',
        '*Missing Info':
            'Please fill all necessary information!..',
        '*Wrong Path':
            'Given save folder address is wrong! Please give a valid path.',
        '*Coins Found':
            'Cryptoassets belonging to exchange are displayed...',
        '*Folder Change':
            'Saving folder has been changed successfully..',
        '*Coin Added':
            'A new cryptoasset has been added successfully..',
        '*Coin Exist':
            'Coin you are trying to add is already existed!..'
    }
