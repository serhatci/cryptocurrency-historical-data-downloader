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
from coin_cls import Coin


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
                self.show_exchange_info(self.__clicked_exc)

            # Assign user selected coin to an attr
            if event == '-coins_table-':
                if self.__clicked_exc is None:
                    self.view.display_defined_msg('*Select Exchange', 'red')
                if self.__clicked_exc.coins is None:
                    self.view.display_defined_msg('*No Coin', 'red')
                else:
                    self.set_clicked_coin(values)

            # Adds a new coin to selected exchange
            if event == '-add_coin-':
                if self.__clicked_exc is None:
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
                if self.__clicked_coin is None:
                    self.view.display_defined_msg('*Select Coin', 'red')
                else:
                    self.download_historical_data(self.__clicked_exc,
                                                  self.__clicked_coin)

            # User clicks delete button and coin data is deleted
            if event == '-delete_coin-':
                if self.__clicked_coin is None:
                    self.view.display_defined_msg('*Select Coin', 'red')
                else:
                    self.remove_coin_from_exchange(self.__clicked_exc,
                                                   self.__clicked_coin)

            # Displays available coins traded in target exchange
            if event == '-available-coins-':
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
                self.model.set_coins_of_exc(self.__clicked_exc)
                self.view.update_coin_tbl(self.__clicked_exc)
                if self.cancel is not False:
                    self.cancel = False
                else:
                    self.view.display_msg(
                        '\nDownload completed!...', 'green', True)

        self.view.window.close()

    def check_available_coins(self, exc):
        """Connects exchange API and gets coins traded in the exchange.

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

        Uses threading module to manage long function loop.

        Args:
            exc (obj): target exchange
            coin (obj) given coin
        """
        if coin.last_update is not None:
            self.view.display_defined_msg('*Already Downloaded', 'red')
        else:
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
                'Frequency': values['-frequency-input-'],
                'LastUpdate': None}

    def remove_coin_from_exchange(self, exc, coin):
        """Removes clicked coin from target exchange.

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
        """Adds user given coin to target exchange.

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
            self.show_exchange_info(self.__clicked_exc)
            self.view.display_defined_msg('*Folder Changed', 'green')

    def show_exchange_info(self, exc):
        """Displays selected exchange info on the screen.

        Args:
            exc (obj): target exchange
        """
        error = self.model.set_coins_of_exc(exc)
        self.view.display_exc_info(exc)
        self.view.update_coin_tbl(exc)
        if error:
            for err in error:
                self.view.display_err(err[1])
                self.view.display_msg(
                    f'{err[0]} can not be read!', 'red', True)

    @staticmethod
    def __time_blocks(limit, start_date, end_date, freq):
        """Creates a list including time span for API data request.

        Args:
            limit (int): maximum API request limit of exchange
            start_date (obj): given start date
            end_date (obj): given end date
            freq (str) : given data download frequency

        Returns:
            blocks (list): time spans between start and end dates.
        """
        CONSTANT = {'minutes': 1, 'hours': 60, 'days': 1440,
                    'weeks': 10080, 'months': 40320}
        interval = limit*CONSTANT[freq]
        blocks = []
        if start_date.shift(minutes=interval) < end_date:
            while start_date < end_date:
                blocks.append(start_date.span('minute', count=interval))
                start_date = start_date.shift(minutes=interval)
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
                    sleep(0.5)  # delay for API request not to be banned
                except (ConnectionError, OSError, ValueError) as err:
                    self.view.window.write_event_value('-ERROR-', err)
                    self.cancel = True
                    break
            else:
                self.view.window.write_event_value('-CANCELLED-', '')
                break
        self.view.window.write_event_value('-FINISHED-', '')


class Model:
    setattr()
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
        """Appends coins existed in OS folder to the given exchange's list.

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
                end_date = backend.read_last_update_from_file(file_path)
                comment = backend.read_file_comment(file_path)
                coin_data = backend.form_new_coin_data(comment, end_date)
            except (ValueError, OSError) as err:
                errors.append([file_path, err])
            else:
                coin = backend.create_coin_obj(exc, coin_data)
                exc.possess_coin(coin)
        return errors

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
        WINDOW_SIZE = (1000, 540)
        self.window = sg.Window('Crypto-exchanges Data Downloader',
                                layout,
                                size=WINDOW_SIZE,
                                finalize=True)

    @staticmethod
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
        if append is None:
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
            f'{exc.website}\n--------\n'
        self.window['-output_panel-'].update(msg,
                                             text_color='green',
                                             append=False)

    def update_coin_tbl(self, exc):
        """Updates coins table acc. to exchange' possessed coins.

        Args:
            exc (obj): given exchange 
        """
        def check(x): return x.format(
            'DD-MM-YYYY hh:mm:ss') if x is not None else '-'

        if exc.coins is []:
            data = [['-', '-', '-', '-', '-']]
        else:
            data = [[coin.name,
                     f'{coin.quote}/{coin.base}',
                     check(coin.last_update),
                     coin.start_date.format('DD-MM-YYYY hh:mm:ss'),
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
        else:
            self.__displayed_msg = msg
            return [msg, False]
