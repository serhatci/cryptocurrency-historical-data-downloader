import os
from os import sep
import pandas as pd
import PySimpleGUI as sg  # GUI framework library
from exchange_base_cls import Exchange
from exchange_classes import *
from screen_layout import Layout


class Controller():
    """Provides controller object of MVC design.
    """

    def __init__(self, model, view):
        """Constructor of Controller class.

        Args:
            model (object): model of MVC design
            view (object): view of MVC design
            __selected_exc (obj): User clicked exchange at run-time
                                (Default to None)
            __selected_coin (obj): User clicked coin at run-time
                                (Default to None)
        """
        self.model = model
        self.view = view
        self.__selected_exc = None
        self.__selected_coin = None

    def start(self):
        # Creates screen layout
        layout = Layout.create(self.model._exc_list,
                               self.model._sys.folder_path,
                               self.model._sys.start_date,
                               self.model._sys.start_hour)

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
                    default_path=self.model._sys.folder_path
                )
                self.model._sys.change_folder_path(new_folder)
                self.view.window['-folder-'].update(new_folder)

            # Displays coins belong to the selected exchange
            # Displays exchange info when it is clicked
            if event == '-exchanges_table-':
                col_num = values['-exchanges_table-'][0]
                self.__selected_exc = self.model._exc_list[col_num]
                self.__selected_exc.coins = self.model.get_coins(
                    self.__selected_exc.name)
                self.view.update_coin_tbl(self.__selected_exc)
                msg = f'{self.__selected_exc.name}\n--------\n' \
                    f'{self.__selected_exc.website}'
                self.view.display(msg, 'green')

            # Assign selected coin to a variable
            if event == '-coins_table-':
                if not self.__selected_exc:
                    self.view.display('*Select Exchange', 'red')
                else:
                    col_num = values['-coins_table-'][0]
                    self.__selected_coin = self.__selected_exc.coins[col_num]

            # User clicks -add- button and a new coin is added
            if event == '-add_coin-':
                if not self.__selected_exc:
                    self.view.display('*Select Exchange', 'red')
                else:
                    coin_name = values['-coin_name-']
                    abbr = values['-abbr-']
                    start_date = self.view.window['-start_date-'].get()
                    start_hour = self.view.window['-start_hour-'].get()

                    if not coin_name == '' or abbr == '':
                        self.model.add_coin(self.__selected_exc,
                                            coin_name,
                                            abbr,
                                            start_date,
                                            start_hour)
                        self.view.update_coin_tbl(self.__selected_exc)
                    else:
                        self.view.display('*Missing Info', 'red')

            # User clicks update button and data starts to download
            if event == '-update_coin-':
                if not self.__selected_coin:
                    self.view.display('*Select Coin')
                else:
                    self.model.download_data(self.__selected_coin)
                    self.view.update_coin_table(self.__selected_exc)

            # User clicks update all button and all data starts to download
            if event == '-update_all-':
                for coin in self.__selected_exc.coins:
                    self.model.download_data(coin)
                    self.view.update_coin_table(self.__selected_exc)

            # User clicks delete button and coin data is deleted
            if event == '-delete_coin-':
                if not self.__selected_coin:
                    self.view.display('*Select Coin', 'red')
                else:
                    self.model.delete_coin(self.__selected_coin)
                    self.view.update_coin_tbl(self.__selected_exc)

        self.view.window.close()


class Model:
    """Provides model object of MVC design.
    """

    def __init__(self, config):
        """Constructor of Model class

        Args:
            config (obg): object of config class keeping
                          configuration attr

        Attr:
            _exc_list (list): list of exchange objects instantiated
                              from exchages_classes.py
            _msg (dict): dictionary of pre-defined messages
        """
        self._sys = config
        self._exc_list = [cls() for cls in Exchange.__subclasses__()]
        self._msg = PredefinedMessages._messages

    @staticmethod
    def create_folder(path):
        if not os.path.isdir(path):
            os.mkdir(path)

    @staticmethod
    def create_file(path, file_name, cols):
        file_path = os.path.join(path, file_name)
        if not os.path.isfile(file_path):
            df = pd.DataFrame(columns=cols)
            df.to_csv(file_path, index=False, sep=';')

    @staticmethod
    def get_coins(selected_exc):
        pass

    def add_coin(self, exc, coin_name,
                 abbr, start_date, start_hour):
        save_directory = os.path.join(self._sys.folder_path, exc.name)
        self.create_folder(save_directory)
        columns = [i['Column Name'] for i in exc.db_columns]
        file_name = f'{coin_name}_{exc.name}_{start_date}.csv'
        self.create_file(save_directory, file_name, columns)


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

    def update_coin_tbl(self, values):
        """Updates coins table in the screen.

        Args:
            values (list): 
        """
        pass


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
