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
            __selected_exc (obj): User clicked exchange at run-time
                                (Default to None)
            __selected_coin (obj): User clicked coin at run-time
                                (Default to None)
        """
        self.model = Model()
        self.view = View()
        self.__selected_exc = None
        self.__selected_coin = None

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
            print(event, values)

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
                self.model.sys.change_folder_path(new_folder)
                self.view.window['-folder-'].update(new_folder)

            # Displays coins belong to the selected exchange
            # Displays exchange info when it is clicked
            if event == '-exchanges_table-':
                col_num = values['-exchanges_table-'][0]
                self.__selected_exc = self.model.exc_list[col_num]
                self.model.check_coins(self.__selected_exc)
                data = self.model.make_displayable(
                    self.__selected_exc.coins)
                self.view.update_coin_tbl(data)
                msg = f'{self.__selected_exc.name}\n--------\n' \
                    f'{self.__selected_exc.website}'
                self.view.display(msg, 'green')

            # Assign selected coin to a variable
            if event == '-coins_table-':
                if not self.__selected_exc:
                    self.view.display(
                        self.model.msg('*Select Exchange'),
                        'red')
                else:
                    col_num = values['-coins_table-'][0]
                    self.__selected_coin = self.__selected_exc.coins[col_num]

            # User clicks -add- button and a new coin is added
            if event == '-add_coin-':
                if not self.__selected_exc:
                    self.view.display(
                        self.model.msg('*Select Exchange'),
                        'red')
                else:
                    if (values['-coin_name-'] == '' or
                            values['-abbr-'] == ''):
                        self.view.display(
                            self.model.msg('*Missing Info'),
                            'red')
                    else:
                        coin_name = values['-coin_name-']
                        abbr = values['-abbr-']
                        start_date = self.view.window['-start_date-'].get()
                        start_hour = self.view.window['-start_hour-'].get()
                        self.model.add_coin(self.__selected_exc,
                                            coin_name,
                                            abbr,
                                            start_date,
                                            start_hour)
                        data = self.model.make_displayable(
                            self.__selected_exc.coins)
                        self.view.update_coin_tbl(data)

            # User clicks update button and data starts to download
            if event == '-update_coin-':
                if not self.__selected_coin:
                    self.view.display(
                        self.model.msg('*Select Coin'),
                        'red')
                else:
                    self.model.download_data(self.__selected_coin)
                    data = self.model.make_displayable(
                        self.__selected_exc.coins)
                    self.view.update_coin_tbl(data)

            # User clicks update all button and all data starts to download
            if event == '-update_all-':
                for coin in self.__selected_exc.coins:
                    self.model.download_data(coin)
                    data = self.model.make_displayable(
                        self.__selected_exc.coins)
                    self.view.update_coin_tbl(data)

            # User clicks delete button and coin data is deleted
            if event == '-delete_coin-':
                if not self.__selected_coin:
                    self.view.display(
                        self.model.msg('*Select Coin'),
                        'red')
                else:
                    self.model.delete_coin(self.__selected_coin)
                    data = self.model.make_displayable(
                        self.__selected_exc.coins)
                    self.view.update_coin_tbl(self.__selected_exc.coins)

        self.view.window.close()


class Model:
    """Provides model object of MVC design.
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
        return cls.__exc_list

    @ staticmethod
    def msg(msg):
        return PredefinedMessages._messages[msg]

    @ staticmethod
    def create_folder(path):
        """Creates a directory in the system.

        Args:
            path (str): path where directory will be created
        """
        if not os.path.isdir(path):
            os.mkdir(path)

    @ staticmethod
    def create_file(path, file_name, cols):
        """Creates cvs files in which downloaded data will be stored.

        Args:
            path (str): path where file will be created
            file_name (str): Name of the file including extension
            cols (list): list of default column names
        """
        file_path = os.path.join(path, file_name)
        if not os.path.isfile(file_path):
            df = pd.DataFrame(columns=cols)
            df.to_csv(file_path, index=False, sep=';')

    def check_coins(self, exc):
        if not exc == {}:
            path = os.path.join(self.sys.folder_path, exc.name)
            if os.path.isdir(path):
                files = os.listdir(path)
                for coin in exc.coins:
                    file_name = '{}_{}_{}.csv'.format(
                        coin,
                        exc.name,
                        exc.coins[coin]['StartDate']
                    )
                    if not file_name in files:
                        exc.set_coins('-', coin)
                        self.sys.save_coins(exc.name, exc.coins)

    def add_coin(self, exc, coin_name,
                 abbr, start_date, start_hour):
        """Adds new coins to the exchange

        Args:
            exc (obj): selected exchange for coin addition
            coin_name (str): name of coin
            abbr (str): abbreviation of coin
            start_date (str): start date
            start_hour (str): start hour
        """
        save_directory = os.path.join(self.sys.folder_path, exc.name)
        self.create_folder(save_directory)
        columns = [i['Column Name'] for i in exc.db_columns]
        file_name = f'{coin_name}_{exc.name}_{start_date}.csv'
        self.create_file(save_directory, file_name, columns)
        coin_data = {'Abbr': abbr,
                     'StartDate': start_date,
                     'StartHour': start_hour,
                     'EndDate': '-',
                     'EndHour': '-'}
        exc.set_coins('+', coin_name, coin_data)
        self.sys.save_coins(exc.name, exc.coins)

    @staticmethod
    def make_displayable(coins):
        if not coins == {}:
            return [[coin,
                     coins[coin]['Abbr'],
                     coins[coin]['EndDate'],
                     coins[coin]['StartDate']] for coin in coins]
        else:
            return [['-', '-', '-', '-']]


class View:
    """Provides view object of MVC design.

    attr:
        window (obj): Pysimplegui window object
    """

    def display(self, msg, color):
        """Displays messages on action panel in the screen.

        Args:
            msg (str): desired message to be displayed
            color (str): desired color of the message
        """
        self.window['-output_panel-'].update(msg,
                                             text_color=color)

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
            'Please fill all necessary information!..'
    }
