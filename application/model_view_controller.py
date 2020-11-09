import PySimpleGUI as sg  # GUI framework library
import filemodel_func as backend
from config_cls import Config
from exchange_base_cls import Exchange
from exchange_classes import *
from predefined_messages import PredefinedMessages
from screen_layout import Layout
import arrow
import threading
from time import sleep


class Controller():
    """Provides controller object of MVC design.
    """

    def __init__(self, model, view):
        """Constructor of Controller class.

        Args:
            model (object): model of MVC design
            view (object): view of MVC design

        Attr:
            __clicked_exc (obj): stores user selected exchange at run-time
                               (Default to None)
            __clicked_coin (obj): stores user selected coin at run-time
                                (Default to None)
        """
        self.model = Model()
        self.view = View()
        self.__clicked_exc = None
        self.__clicked_coin = None
        self.cancel = False

    def start_app(self):
        """Starts application
        """

        # Creates screen layout
        end_date = arrow.utcnow().format('DD-MM-YYYY')
        end_hour = arrow.utcnow().format('HH:mm:ss')
        layout = Layout.create(self.model.exc_list,
                               self.model.sys.save_path,
                               self.model.sys.start_date,
                               self.model.sys.start_hour,
                               end_date,
                               end_hour)

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
                new_folder = self.get_new_save_folder()
                self.change_save_path(new_folder)

            # Displays related info for user selected exchange
            if event == '-exchanges_table-':
                self.set_clicked_exchange(values)
                self.show_clicked_exc_info()

            # Assign user selected coin to an attr
            if event == '-coins_table-':
                if not self.__clicked_exc:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                if not self.__clicked_exc.coins:
                    self.view.display_defined_msg('*No Coin', 'red')
                else:
                    self.set_clicked_coin(values)

            # Adds a new coin to selected exchange
            if event == '-add_coin-':
                if not self.__clicked_exc:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                elif values['-coin_name-'] == '':
                    self.view.display_defined_msg('*Missing Name', 'red')
                elif values['-quote-'] == '':
                    self.view.display_defined_msg('*Missing Quote', 'red')
                elif values['-base-'] == '':
                    self.view.display_defined_msg('*Missing Base', 'red')
                else:
                    coin_data = self.collect_user_input(values)
                    self.add_new_coin_to_exchange(coin_data)

            # Changes cancel attr. to stop data download
            if event == '-cancel-':
                self.cancel = True

            # Downloads coins data starts to download
            if event == '-download_coin-':
                if not self.__clicked_coin:
                    self.view.display_defined_msg('*Select Coin', 'red')
                else:
                    self.download_historical_data()
                    self.__clicked_coin = None

            # Displays progress of data download
            if event == '-PROGRESS-':
                msg = f"Part {values['-PROGRESS-']}: downloaded & saved!\n"
                self.view.display_msg(msg, 'orange', True)

            # Displays success message after data download finished
            if event == '-FINISHED-':
                self.view.display_msg(
                    '\nDownload successfully completed!..', 'green', True)
                self.view.update_coin_tbl(self.__clicked_exc)

            # User clicks delete button and coin data is deleted
            if event == '-delete_coin-':
                if not self.__clicked_coin:
                    self.view.display_defined_msg('*Select Coin', 'red')
                else:
                    self.remove_coin_from_exchange()

            # Displays available coins traded in target exchange
            if event == '-available-coins-':
                if not self.__clicked_exc:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                else:
                    self.check_available_coins()

        self.view.window.close()

    def check_available_coins(self):
        """Connects exchange API and gets coins traded in the exchange.
        """
        try:
            coins = self.__clicked_exc.provide_available_coins()
        except ConnectionError as err:
            self.view.display_err(err)
        else:
            self.view.display_msg(
                f'Available coins:\n{coins}', 'green')

    def download_historical_data(self):
        """Downloads historical coin data from exchange API.

        Uses threading module to manage long function loop.
        """
        blocks = self.model.get_download_time_blocks(
            self.__clicked_exc, self.__clicked_coin)
        self.view.display_defined_msg(
            '*Down Start', 'green', f'{len(blocks)} PARTS\n', False)
        threading.Thread(target=self.__download,
                         args=(self.__clicked_exc,
                               self.__clicked_coin,
                               blocks),
                         daemon=True).start()

    def __download(self, exc, coin, blocks):
        """Downloads and saves coin data.

        Args:
            exc (obj): given exchange
            coin (obj): given coin
            blocks (list): time blocks for download request
        """
        for part, time in enumerate(blocks):
            if not self.cancel:
                try:
                    data = exc.download_hist_data(coin, time)
                    self.model.save_downloaded_data(exc, coin, data)
                    self.view.window.write_event_value('-PROGRESS-', part+1)
                    sleep(1)
                except ConnectionError as err:
                    self.view.display_err(err)
            else:
                self.view.display_defined_msg('*Cancelled', 'red')
                self.model.delete_coin(exc, coin)
                self.view.update_coin_tbl(exc)
                break
        if self.cancel:
            self.cancel = False
        else:
            self.view.window.write_event_value('-FINISHED-', '')

    def collect_user_input(self, values):
        """Collects user inputs for new coin.

        Args:
            values (dict): values collected from app window

        Returns:
            dict: coin data for obj creation
        """
        return {'Name': values['-coin_name-'],
                'Quote': values['-quote-'],
                'Base': values['-base-'],
                'StartDate': self.view.window['-start_date-'].get(),
                'StartHour': self.view.window['-start_hour-'].get(),
                'EndDate': self.view.window['-end_date-'].get(),
                'EndHour': self.view.window['-end_hour-'].get(),
                'Frequency': values['-frequency-input-']}

    def remove_coin_from_exchange(self):
        """Removes clicked coin from target exchange.
        """
        try:
            self.model.delete_coin(self.__clicked_exc,
                                   self.__clicked_coin)
        except OSError as err:
            self.view.display_err(err)
        else:
            self.view.display_defined_msg(
                '*Coin Deleted',
                'green',
                self.__clicked_coin.name.upper(),
                False)
            self.view.update_coin_tbl(self.__clicked_exc)
            self.__clicked_coin = None

    def add_new_coin_to_exchange(self, coin_data):
        """Adds user given coin to target exchange.

        Arg:
            coin_data (dict): data of coin being added 
        """
        try:
            self.model.add_coin(self.__clicked_exc, coin_data)
        except (FileExistsError, OSError) as err:
            self.view.display_err(err)
        else:
            self.view.display_defined_msg('*Coin Added',
                                          'green',
                                          coin_data['Name'].upper())
            self.view.update_coin_tbl(self.__clicked_exc)

    def set_clicked_coin(self, values):
        """Stores user selected coin in __clicked_coin attr.

        Args:
            values (dict): values collected from app window
        """
        col_num = values['-coins_table-'][0]
        self.__clicked_coin = self.__clicked_exc.coins[col_num]

    def set_clicked_exchange(self, values):
        """Stores user selected exchange in __clicked_exc attr.

        Args:
            values (dict): values collected from app window
        """
        col_num = values['-exchanges_table-'][0]
        self.__clicked_exc = self.model.exc_list[col_num]

    def get_new_save_folder(self):
        """Gets new save folder path from user.

        Returns:
            str: new save folder path
        """
        default_path = self.model.sys.save_path
        new_folder = self.view.pop_up_folder(default_path)
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
            self.show_clicked_exc_info()
            self.view.display_defined_msg('*Folder Changed', 'green')

    def show_clicked_exc_info(self):
        """Displays selected exchange info on the screen.
        """
        error = self.model.set_coins_of_exc(self.__clicked_exc)
        self.view.display_exc_info(self.__clicked_exc)
        self.view.update_coin_tbl(self.__clicked_exc)
        if error:
            for err in error:
                self.view.display_err(err[1])
                self.view.display_msg(
                    f'{err[0]} can not be read!', 'red', True)


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

    def set_coins_of_exc(self, exc):
        """Appends coins found in given exchange's folder to exchange list.

        Args:
            exc (obj): target exchange

        Returns:
            error (list): contains file name and errors occurred when reading
                          a coin file.
        """
        exc.coins = []  # empties exchange coins list
        errors = []
        coin_file_paths = backend.get_coin_files(exc, self.sys.save_path)
        for file_path in coin_file_paths:
            try:
                comment = backend.read_file_comment(file_path)
                coin_data = backend.form_new_coin_data(comment)
            except (ValueError, OSError) as err:
                errors.append([file_path, err])
            else:
                coin = backend.create_coin_obj(exc, coin_data)
                exc.possess_coin(coin)
        return errors

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

    def delete_coin(self, exc, coin):
        """Deletes the coin file from OS and exchange.

        Args:
            exc (obj): exchange object
            coin (obj): coin object
        """
        backend.delete_coin_file(exc, coin, self.sys.save_path)
        if not backend.get_coin_files(exc, self.sys.save_path):
            backend.delete_exc_folder(exc, self.sys.save_path)
        exc.abandon_coin(coin)

    def save_downloaded_data(self, exc, coin, data):
        """Saves downloaded coin data to csv file.

        Args:
            exc (obj): given exchange
            coin (obj): target coin
            data (list): downloaded coin data
        """
        backend.save_data(exc, coin, data, self.sys.save_path)

    def get_download_time_blocks(self, exc, coin):
        """Creates time spans for data request.

        Args:
            exc (obj): given exchange
            coin (obj): given coin 

        Returns:
            list: time spans for API data request
        """
        start_date, end_date = self.__get_date_objects(coin)
        add = exc.max_API_requests
        freq = coin.frequency
        if self.__increase_time(start_date, add, freq) > end_date:
            return [[start_date, end_date]]
        else:
            blocks = []
            while self.__increase_time(start_date, add+1, freq) < end_date:
                blocks.append([start_date,
                               self.__increase_time(start_date, add, freq)])
                start_date = self.__increase_time(start_date, add+1, freq)
            blocks.append([start_date, end_date])
            return blocks

    @ staticmethod
    def __get_date_objects(coin):
        """__Converts string date to arrow objects.

        Args:
            coin (obj): given coin

        Returns:
            obj : start date, end date 
        """
        fmt = 'DD-MM-YYYY HH:mm:ss'
        start_date = arrow.get(coin.start_date + ' '+coin.start_hour, fmt)
        end_date = arrow.get(coin.end_date + ' ' + coin.end_hour, fmt)
        return start_date, end_date

    @ staticmethod
    def __increase_time(date, incremental, freq):
        """Increases date acc. to user preferences.

        Args:
            date (obj): given date
            incremental (int): aimned increase in time 
            freq (str): days, hours, minutes etc... 

        Returns:
            obj: date increased by incremental value
        """
        if freq == 'minutes':
            return date.shift(minutes=incremental)
        if freq == 'hours':
            return date.shift(hours=incremental)
        if freq == 'days':
            return date.shift(days=incremental)
        if freq == 'weeks':
            return date.shift(weeks=incremental)
        if freq == 'months':
            return date.shift(months=incremental)


class View:
    """Provides view object of MVC design.

    attr:
        __displayed_msg (obj): stores displayed messages at run-time
    """
    __displayed_msg = None

    def start_window(self, layout):
        """Starts application window.

        Args:
            layout (obj): PysimpleGUI layout
        """
        WINDOW_SIZE = (1000, 540)
        self.window = sg.Window('Crypto-exchanges Data Downloader',
                                layout,
                                size=WINDOW_SIZE,
                                finalize=True)

    def pop_up_folder(self, default_path):
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

    def display_msg(self, msg, color, value=None):
        """Displays given message at output panel on the screen.

        Args:
            msg_key (str): short description of pre-defined message
            color (str): desired color of the message
        """
        if not value:
            msg, value = self.__check_repeating_msg(msg)
        self.window['-output_panel-'].update(msg,
                                             text_color=color,
                                             append=value)

    def display_defined_msg(self, msg_key, color, arg=None, append=None):
        """Displays a pre-defined message at output panel on the screen.

        Args:
            msg_key (str): short description of pre-defined message
            color (str): desired color of the message
            arg (str): additional argument to be displayed
                  (default to None)
            append (str): optional append value
                        (default to None)
        """
        msg = PredefinedMessages._messages[msg_key]
        if append == None:
            msg, append = self.__check_repeating_msg(msg)
        self.window['-output_panel-'].update(msg,
                                             text_color=color,
                                             append=append)
        if arg:
            self.window['-output_panel-'].update('\n'+arg,
                                                 append=True)

    def display_err(self, err_msg):
        """Displays error messages at output panel on the screen.

        Args:
            err_msg (str): err_msg message to be displayed
        """
        msg = f'{err_msg}'
        msg, value = self.__check_repeating_msg(msg)
        self.window['-output_panel-'].update(msg,
                                             text_color='red',
                                             append=value,
                                             autoscroll=True)

    def display_exc_info(self, exc):
        """Displays exchange specific info at output panel.

        Args:
            exc (obj): user selected exchange
        """
        msg = f'\n{exc.name}\n--------\n' \
            f'{exc.website}\n--------\n'
        self.window['-output_panel-'].update(msg,
                                             text_color='green',
                                             append=False)

    def update_coin_tbl(self, exc):
        """Updates coins table acc. to exchange' possessed coins.

        Args:
            exc (obj): exchange bj
        """
        if not exc.coins:
            data = [['-', '-', '-', '-', '-']]
        else:
            data = [[coin.name,
                     coin.quote+'-'+coin.base,
                     coin.start_date,
                     coin.end_date,
                     coin.frequency] for coin in exc.coins]

        self.window['-coins_table-'].update(data)

    def create_coin_obj(self, values):
        """Collect user inputs and creates a coin obj

        Args:
            values (dict): values collected from app window

        Returns:
            obj: new coin obj
        """
        return Coin(self.__clicked_exc, coin_data)

    def __check_repeating_msg(self, msg):
        """Checks if msg is already displayed on the screen.

        If message is displayed, changes the msg and append value.

        Args:
            msg (str): msg to be displayed

        Returns:
            (list): msg and append value
        """
        if self.__displayed_msg == msg:
            msg = '\n----------------------\n' + msg
            return [msg, True]
        else:
            self.__displayed_msg = msg
            return [msg, False]
