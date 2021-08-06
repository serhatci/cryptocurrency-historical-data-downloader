''' Provides classes of MVC design.

List of Classes:
    Controller
    Model
    View
'''

import re  # regular expression
import threading
from datetime import timedelta
from time import sleep

import arrow  # datetime management
import PySimpleGUI as sg  # GUI framework library

import application.filemodel_func as backend
from application.classes.coin_cls import Coin
from application.classes.config_cls import Config
from application.classes.exchange_base_cls import Exchange
from application.classes.exchange_classes import *
from application.predefined_messages import PredefinedMessages
from application.screen_layout import Layout


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
            cancel (bool): stores state of cancel button
        """
        self.model = model
        self.view = view
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

        This function completely depends on the provided format of
        PySimpleGUI framework.
        see for more: https://pysimplegui.readthedocs.io/en/latest/#jump-start
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
                self.show_exchange_info(self.__clicked_exc)

            # Assign user selected coin to an attr
            if event == '-coins_table-':
                if self.__clicked_exc is None:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                elif not self.__clicked_exc.coins:
                    self.view.display_defined_msg('*No Coin', 'red')
                else:
                    self.set_clicked_coin(values)

            # Adds a new coin to selected exchange
            if event == '-add_coin-':
                if self.__clicked_exc is None:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                else:
                    coin_data = self.collect_user_input(values)
                    if (self.__input_error(coin_data['Name'],
                                           coin_data['Quote'],
                                           coin_data['Base']) is False and
                            self.__date_error(coin_data) is False):
                        self.add_new_coin_to_exchange(coin_data)

            # Changes cancel attr. to stop data download
            if event == '-cancel-':
                self.cancel = True

            # Downloads coins data starts to download
            if event == '-download_coin-':
                if self.__clicked_coin is None:
                    self.view.display_defined_msg('*Select Coin', 'red')
                elif self.__clicked_coin.last_update is not None:
                    self.view.display_defined_msg(
                        '*Already Downloaded', 'red')
                else:
                    self.download_historical_data(self.__clicked_exc,
                                                  self.__clicked_coin)
                    self.__clicked_coin = None

            # Updates downloaded coin data to present date
            if event == '-update_coin-':
                if self.__clicked_coin is None:
                    self.view.display_defined_msg('*Select Coin', 'red')
                elif self.__clicked_coin.last_update is None:
                    self.view.display_defined_msg('*No Update', 'red')
                else:
                    self.update_historical_data(self.__clicked_exc,
                                                self.__clicked_coin)
                    self.__clicked_coin = None

            # User clicks delete button and coin data is deleted
            if event == '-delete_coin-':
                if self.__clicked_coin is None:
                    self.view.display_defined_msg('*Select Coin', 'red')
                else:
                    self.remove_coin_from_exchange(self.__clicked_exc,
                                                   self.__clicked_coin)

            # Displays available coins traded in target exchange
            if event == '-available_coins-':
                if self.__clicked_exc is None:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                else:
                    self.check_available_coins(self.__clicked_exc)

            # Displays progress of data download
            if event == '-PROGRESS-':
                msg = "Part {} of {}: downloaded & saved!\n".format(
                    values['-PROGRESS-'][0], values['-PROGRESS-'][1])
                self.view.display_msg(msg, 'orange', True)

            # Displays errors of data download
            if event == '-ERROR-':
                self.view.display_err(values['-ERROR-'])

            # Displays info if data download is cancelled
            if event == '-CANCELLED-':
                self.view.display_defined_msg('*Cancelled', 'red')

            # Displays success message after data download finished
            if event == '-FINISHED-':
                if self.cancel is not False:
                    self.cancel = False
                else:
                    self.view.display_msg(
                        '\nDownload completed!...', 'green', True)
                self.set_coins_of_exchange(self.__clicked_exc)
                self.view.update_coin_tbl(self.__clicked_exc)

        self.view.window.close()

    def __date_error(self, coin):
        """Checks if there is error in the date inputs of user.

        Args:
            coin (dict): user given coin data

        Returns:
            (bool): return True if there is an error in inputs
        """
        try:
            fmt = 'DD-MM-YYYY HH:mm:ss'
            start = arrow.get(
                f"{coin['StartDate']} {coin['StartHour']}", fmt)
            end = arrow.get(
                f"{coin['EndDate']} {coin['EndHour']}", fmt)
        except ValueError:
            self.view.display_defined_msg('*Format Err', 'red')
            return True
        else:
            if not start < end:
                self.view.display_defined_msg('*Date Err', 'red')
                return True
            return False

    def __input_error(self, name, quote, base):
        """Checks if the inputs are correct for further execution.

        Args:
            name (str): coin name
            quote (str): quote coin abbreviation
            base (str): base coin abbreviation

        return:
            (bool): return True if there is an error in inputs
        """
        def check(x): return True if (
            x == '' or bool(re.search("[^a-zA-Z0-9\s]+", x))) else False
        val_err = False
        if check(name) is True:
            self.view.display_defined_msg('*Name Err', 'red')
            val_err = True
        elif (check(quote) or check(base)) is True:
            self.view.display_defined_msg('*Quote-Base Err', 'red', '', False)
            val_err = True
        return val_err

    def check_available_coins(self, exc):
        """Connects to exchange API and gets current coins traded.

        Args:
            exc (obj): target exchange
        """
        try:
            coins = exc.provide_available_coins()
        except ConnectionError as err:
            self.view.display_err(err)
        else:
            self.view.display_msg(
                f'Available coins:\n{coins}', 'green')

    def download_historical_data(self, exc, coin):
        """Downloads historical coin data from exchange API.

        Uses threading module to manage long function loop. Threading behavior
        is a part of PYsimpleGUI library. see below for more:
        https://pysimplegui.readthedocs.io/en/latest/

        Args:
            exc (obj): target exchange
            coin (obj) given coin
        """
        try:
            blocks = self.__time_blocks(exc.max_API_requests,
                                        coin.start_date,
                                        coin.end_date,
                                        coin.frequency)
            self.view.display_defined_msg(
                '*Down Start',
                'green',
                f'-----{len(blocks)} PARTS-----\n',
                False)
            threading.Thread(target=self.__download,
                             args=(exc, coin, blocks),
                             daemon=True).start()
        except (ValueError, OSError) as err:
            self.view.display_err(err)

    def update_historical_data(self, exc, coin):
        """Updates downloaded historical data to the present date.

        Args:
            exc (obj): target exchange
            coin (obj) given coin
        """
        coin.start_date = coin.last_update
        coin.end_date = arrow.utcnow()
        self.download_historical_data(exc, coin)

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
                'Frequency': values['-frequency_input-'],
                'LastUpdate': None}

    def remove_coin_from_exchange(self, exc, coin):
        """Removes clicked coin from the target exchange.

        Args:
            exc (obj): target exchange
            coin (obj): given coin
        """
        try:
            self.model.delete_coin(exc, coin)
        except OSError as err:
            self.view.display_err(err)
        else:
            self.view.display_defined_msg('*Coin Deleted',
                                          'green',
                                          coin.name.upper(),
                                          False)
            self.view.update_coin_tbl(exc)
            self.__clicked_coin = None

    def add_new_coin_to_exchange(self, coin_data):
        """Adds user given coin to the target exchange.

        Arg:
            coin_data (dict): data of coin being added
        """
        try:
            new_coin = Coin(self.__clicked_exc, coin_data)
            self.model.add_coin(self.__clicked_exc, new_coin)
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
            if self.__clicked_exc:
                self.show_exchange_info(self.__clicked_exc)
            self.view.display_defined_msg('*Folder Changed', 'green')

    def show_exchange_info(self, exc):
        """Displays selected exchange info on the screen.

        Args:
            exc (obj): target exchange
        """
        self.view.display_exc_info(exc)
        self.view.set_resolution(exc.resolution)
        error = self.set_coins_of_exchange(exc)
        for err in error:
            self.view.display_msg(err, 'orange', True)
        self.view.update_coin_tbl(exc)

    def set_coins_of_exchange(self, exc):
        """Gets coins of exchange from relevant database and add them to exc.

        Args:
            exc (obj): target exchange

        return:
            error (list): errors occurred in setting of exchange coins
        """
        exc.coins = []  # empties exchange coins list
        coin_data, error = self.model.read_coins_data(exc)
        for coin in coin_data:
            exc.possess_coin(Coin(exc, coin))
        return error

    @ staticmethod
    def __time_blocks(limit, start_date, end_date, freq):
        """Creates a list including time span for API data request.

        API of some exchanges allow requesting limited number of data per time.
        __time_blocks function creates a bunch of time periods which helps
        application to downloads all historical data with sequencing requests.

        Args:
            limit (int): maximum API request limit of exchange
            start_date (obj): given start date
            end_date (obj): given end date
            freq (str) : given data download frequency

        Returns:
            blocks (list): time spans between start and end dates.
        """
        def select(freq):
            if freq == 'minutes':
                return timedelta(minutes=1)
            if freq == 'hours':
                return timedelta(hours=1)
            if freq == 'days':
                return timedelta(days=1)
            if freq == 'weeks':
                return timedelta(weeks=1)
            if freq == 'months':
                return timedelta(weeks=4)

        interval = select(freq)*limit
        blocks = []
        if (start_date+interval) < end_date:
            while start_date < end_date:
                blocks.append(
                    [start_date, start_date+interval])
                start_date = start_date+interval
            blocks[-1][1] = end_date
        else:
            blocks.append((start_date, end_date))
        return blocks

    def __download(self, exc, coin, blocks):
        """Downloads and saves coin data.

        Args:
            exc (obj): given exchange
            coin (obj): given coin
            blocks (list): time blocks for download request
        """
        for part, time in enumerate(blocks):
            if self.cancel is False:
                try:
                    data = exc.download_hist_data(coin, time)
                    self.model.save_downloaded_data(exc, coin, data)
                    info = (part+1, len(blocks))
                    self.view.window.write_event_value('-PROGRESS-', info)
                    sleep(0.5)  # delay for request not to be banned by API
                except (ConnectionError, OSError, ValueError) as err:
                    self.view.window.write_event_value('-ERROR-', err)
                    self.cancel = True
                    break
            else:
                self.view.window.write_event_value('-CANCELLED-', '')
                break
        self.view.window.write_event_value('-FINISHED-', '')


class Model:
    """Provides model object of MVC design.

    class attr:
        __exc_list (list): list of exchange objects
        __sys (obj) : object that stores configuration data
    """

    __exc_list = [cls() for cls in Exchange.__subclasses__()]
    __sys = Config()

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

    def read_coins_data(self, exc):
        """read coin data by reading existed coin files in exchange's folder.

        Args:
            exc (obj): target exchange

        Returns:
            coins, errors (list,list): coin data and errors occurred
                                       when reading coin files.
        """
        errors = []
        coins = []
        coin_file_paths = backend.get_coin_files(exc, self.sys.save_path)
        for file_path in coin_file_paths:
            try:
                end_date = backend.read_last_update_from_file(file_path)
                comment = backend.read_file_comment(file_path)
                coin_data = backend.form_new_coin_data(comment, end_date)
            except (ValueError, OSError) as err:
                errors.append(err)
            else:
                coins.append(coin_data)
        return coins, errors

    def add_coin(self, exc, new_coin):
        """Adds a coin to the exchange and saves its csv file.

        Args:
            exc (obj): selected exchange for coin addition
            new_coin (obj): new coin will be added to exchange
        """
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
        WINDOW_SIZE = (1000, 560)
        self.window = sg.Window('Crypto-exchanges Data Downloader',
                                layout,
                                size=WINDOW_SIZE,
                                finalize=True)

    @ staticmethod
    def pop_up_folder(default_path):
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

    def display_msg(self, msg, color, append=None):
        """Displays given message at output panel on the screen.

        Args:
            msg (str): given message to display
            color (str): desired color of the message
            append (bool): append variable of update method
                           (default to None)
        """
        if append is None:
            msg, append = self.__check_repeating_msg(msg)
        self.window['-output_panel-'].update(msg,
                                             text_color=color,
                                             append=append)

    def display_defined_msg(self, msg_key, color, arg=None, append=False):
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
        if append is False:
            msg, append = self.__check_repeating_msg(msg)
        self.window['-output_panel-'].update(msg,
                                             text_color=color,
                                             append=append)
        if arg is not None:
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
            f'{exc.website}\n--------\n' \
            f'{exc.common_info}'
        self.window['-output_panel-'].update(msg,
                                             text_color='green',
                                             append=False)
        self.__displayed_msg = None

    def update_coin_tbl(self, exc):
        """Updates coins table acc. to exchange' possessed coins.

        Args:
            exc (obj): given exchange
        """
        def check(x): return x.format(
            'DD-MM-YYYY HH:mm:ss') if x is not None else '-'

        if not exc.coins:
            data = [['-', '-', '-', '-', '-']]
        else:
            data = [[coin.name,
                     f'{coin.quote}/{coin.base}',
                     check(coin.last_update),
                     coin.start_date.format('DD-MM-YYYY HH:mm:ss'),
                     coin.frequency] for coin in exc.coins]

        self.window['-coins_table-'].update(data)

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
        self.__displayed_msg = msg
        return [msg, False]

    def set_resolution(self, res):
        """Updates comboinput element values.

        Args:
            res (tuple): exchange specific resolution data
        """
        self.window['-frequency_input-'].update(values=res)
