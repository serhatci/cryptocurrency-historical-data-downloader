import PySimpleGUI as sg  # GUI framework library
import filemodel_func as backend
from config_cls import Config
from exchange_base_cls import Exchange
from exchange_classes import *
from predefined_messages import PredefinedMessages
from screen_layout import Layout


class Controller():
    """Provides controller object of MVC design.
    """

    def __init__(self, model, view):
        """Constructor of Controller class.

        Args:
            model (object): model of MVC design
            view (object): view of MVC design

        Attr:
            clicked_exc (obj): User selected exchange at run-time
                               (Default to None)
            clicked_coin (obj): User selected coin at run-time
                                (Default to None)
        """
        self.model = Model()
        self.view = View()
        self.clicked_exc = None
        self.clicked_coin = None

    def start_app(self):
        """Starts application
        """

        # Creates screen layout
        layout = Layout.create(self.model.exc_list,
                               self.model.sys.save_path,
                               self.model.sys.start_date,
                               self.model.sys.start_hour)

        # Starts window
        self.view.start_window(layout)

        # Listens the window and collects user inputs
        self.listen_window()

    def listen_window(self):
        """Listens the application window and collects user inputs
        """
        while True:
            event, values = self.view.window.read()

            # Terminates app when user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break

            # Changes save folder acc. to user input
            if event == '-change_folder-':
                new_folder = self.get_new_folder()
                self.change_save_path(new_folder)

            # Displays related info for user selected exchange
            if event == '-exchanges_table-':
                self.set_clicked_exchange(values)
                self.show_clicked_exc_info()

            # Assign user selected coin to an attr
            if event == '-coins_table-':
                if not self.clicked_exc:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                if not self.clicked_exc.coins:
                    self.view.display_defined_msg('*No Coin', 'red')
                else:
                    self.set_clicked_coin(values)

            # Adds a new coin to selected exchange
            if event == '-add_coin-':
                if not self.clicked_exc:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                elif values['-coin_name-'] == '':
                    self.view.display_defined_msg('*Missing Name', 'red')
                elif values['-abbr-'] == '':
                    self.view.display_defined_msg('*Missing Abbr', 'red')
                else:
                    coin_data = self.collect_user_input(values)
                    self.add_new_coin_to_exchange(coin_data)

            # Update coins data starts to download
            if event == '-update_coin-':
                if not self.clicked_coin:
                    self.view.display_defined_msg('*Select Coin', 'red')
                self.model.download_data()
                self.view.update_coin_tbl()

            # User clicks update all button and all data starts to download
            if event == '-update_all-':
                for coin in self.clicked_exc.coins:
                    self.model.download_data(coin)
                self.view.update_coin_tbl()

            # User clicks delete button and coin data is deleted
            if event == '-delete_coin-':
                if not self.clicked_coin:
                    self.view.display_defined_msg('*Select Coin', 'red')
                self.remove_coin_from_exchange()

        self.view.window.close()

    def collect_user_input(self, values):
        """Collects user inputs for new coin.

        Args:
            values (dict): values collected from app window

        Returns:
            dict: coin data for obj creation
        """
        return {
            'Name': values['-coin_name-'],
            'Abbr': values['-abbr-'],
            'StartDate': self.view.window['-start_date-'].get(),
            'StartHour': self.view.window['-start_hour-'].get(),
            'EndDate': '-',
            'EndHour': '-'
        }

    def remove_coin_from_exchange(self):
        """Removes clicked coin from target exchange.
        """
        try:
            self.model.delete_coin(self.clicked_exc, self.clicked_coin)
        except OSError as err:
            self.view.display_err(err)
        else:
            self.view.display_defined_msg('*Coin Deleted', 'green')
            self.view.update_coin_tbl(self.clicked_exc)

    def add_new_coin_to_exchange(self, coin_data):
        """Adds user given coin to target exchange.
        """
        try:
            self.model.add_coin(self.clicked_exc, coin_data)
        except (FileExistsError, OSError) as err:
            self.view.display_err(err)
        else:
            self.view.display_defined_msg('*Coin Added', 'green')
            self.view.update_coin_tbl(self.clicked_exc)

    def set_clicked_coin(self, values):
        """Stores user selected coin in clicked_coin attr

        Args:
            values (dict): values collected from app window
        """
        col_num = values['-coins_table-'][0]
        self.clicked_coin = self.clicked_exc.coins[col_num]

    def set_clicked_exchange(self, values):
        """Stores user selected exchange in clicked_exc attr

        Args:
            values (dict): values collected from app window
        """
        col_num = values['-exchanges_table-'][0]
        self.clicked_exc = self.model.exc_list[col_num]

    def get_new_folder(self):
        """Gets new folder path from user

        Returns:
            str: new folder path
        """
        default_path = self.model.sys.save_path
        new_folder = self.view.pop_up(default_path)
        return new_folder

    def change_save_path(self, new_folder):
        """Changes save folder path acc. to user input.

        Args:
            new_folder (str): path of new save folder
        """
        try:
            self.model.sys.change_save_path(new_folder)
        except (NotADirectoryError, OSError) as err:
            self.view.display_err(err)
        else:
            self.view.update_folder(new_folder)
            self.view.display_defined_msg('*Folder Changed', 'green')
            self.show_clicked_exc_info()

    def show_clicked_exc_info(self):
        """Displays selected exchange info on the screen.
        """
        try:
            result = self.model.check_coins(self.clicked_exc)
            if result:
                self.view.display_defined_msg('*Corrupted Coin', 'orange')
                self.view.display_msg(str(result)[1:-1], 'red')
        except (NotADirectoryError, OSError) as err:
            self.view.display_err(err)
        else:
            self.view.display_exc_info(self.clicked_exc)
            self.view.update_coin_tbl(self.clicked_exc)


class Model:
    """Provides model object of MVC design.

    class attr:
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

    def check_coins(self, exc):
        """Compare coins in memory and coin files in the OS.

        Checks if coin files of clicked exchange in OS match
        with the coins in memory. If there are missing files,
        excludes them from memory.

        Args:
            exc (obj): object of exchange

        Returns:
            excluded_coins (list): removed coins from exchange' coin list
        """
        self.sys.set_coins_of_exchange(exc)
        if exc.coins:
            coin_files = backend.get_coin_files(exc, self.sys.save_path)
            return backend.remove_missing_coins(exc, coin_files)

    def add_coin(self, exc, coin_data):
        """Adds a coin to the exchange and saves its csv file.

        Args:
            exc (obj): selected exchange for coin addition
            coin (obj): target coin
        """
        new_coin = backend.create_coin_obj(exc, coin_data)
        backend.create_exc_folder(exc, self.sys.save_path)
        backend.create_coin_file(exc, new_coin, self.sys.save_path)
        exc.possess_coin(new_coin)
        self.sys.update_config_file(exc)

    def delete_coin(self, exc, coin):
        """Deletes the coin file from OS and exchange.

        Args:
            exc (obj): exchange object
            coin (obj): coin object
        """
        backend.delete_coin_file(exc, coin, self.sys.save_path)
        if not backend.files_in_folder(exc, self.sys.save_path):
            backend.delete_exc_folder(exc, self.sys.save_path)
        exc.abandon_coin(coin)
        self.sys.update_config_file(exc)


class View:
    """Provides view object of MVC design.
    """

    def start_window(self, layout):
        """Starts application window.

        Args:
            layout (obj): PysimpleGUI layout
        """
        WINDOW_SIZE = (1000, 520)
        self.window = sg.Window('Crypto-exchanges Data Downloader',
                                layout,
                                size=WINDOW_SIZE,
                                finalize=True)

    def pop_up(self, default_path):
        """Opens a pop-up window to get new save folder.

        Args:
            default_path (str): default save folder path

        Returns:
            str: new save folder path
        """
        return sg.popup_get_folder(
            'Select a folder to save downloaded data',
            title='Browse Folder',
            default_path=default_path)

    def update_folder(self, new_folder):
        """Updates save folder path in the screen.

        Args:
            new_folder (str): path of new folder
        """
        self.window['-folder-'].update(new_folder)

    def display_msg(self, msg, color):
        """Displays given message at output panel on the screen.

        Args:
            msg_key (str): short description of pre-defined message
            color (str): desired color of the message
        """
        self.window['-output_panel-'].update(msg,
                                             text_color=color,
                                             append=True)

    def display_defined_msg(self, msg_key, color):
        """Displays a pre-defined message at output panel on the screen.

        Args:
            msg_key (str): short description of pre-defined message
            color (str): desired color of the message
        """
        msg = PredefinedMessages._messages[msg_key]
        self.window['-output_panel-'].update(msg,
                                             text_color=color,
                                             append=True)

    def display_err(self, err_msg):
        """Displays error messages at output panel on the screen.

        Args:
            err_msg (str): err_msg message to be displayed
        """
        msg = 'A problem occurred during execution:' \
              f'\n-----------\n{err_msg}\n------------\n'
        self.window['-output_panel-'].update(msg,
                                             text_color='red',
                                             append=True)

    def display_exc_info(self, exc):
        """Displays exchange specific info at output panel.

        Args:
            exc (obj): user selected exchange
        """
        msg = f'\n{exc.name}\n--------\n' \
            f'{exc.website}\n--------\n'
        self.window['-output_panel-'].update(msg,
                                             text_color='green',
                                             append=True)

    def update_coin_tbl(self, exc):
        """Updates coins table acc. to exchange' possessed coins.

        Args:
            exc (obj): exchange bj
        """
        if not exc.coins:
            data = [['-', '-', '-', '-']]
        else:
            data = [[coin.name,
                     coin.abbr,
                     coin.end_date,
                     coin.start_date] for coin in exc.coins]

        self.window['-coins_table-'].update(data)

    def create_coin_obj(self, values):
        """Collect user inputs and creates a coin obj

        Args:
            values (dict): values collected from app window

        Returns:
            obj: new coin obj
        """
        return Coin(self.clicked_exc, coin_data)
