"""Provides a base class for creating crypto-exchange classes.

    List of classes:
        Exchange
    """
from abc import ABC, abstractmethod


class Exchange(ABC):
    """An abstract base class to create crypto-exchange classes.

    class attr:
        __instance (obj): keeps instance of Exchange class to
                          app singleton pattern
                          (Default to None)
    """

    __instance = None

    def __new__(cls):
        """Creates only a single instance of class.

        Singleton design pattern.

        Raises:
            Exception: occurs when a second instance
                       is tried to be created

        Returns:
            object: crypto exchage object
        """

        if not cls.__instance:
            cls.__instance = super(Exchange, cls).__new__(cls)
            return cls.__instance
        else:
            raise Exception(
                f'{cls.__instance.name} was already created!..')

    def __init__(self):
        """Constructor of Exchange class.

        Attr:
            __coins (list): list of coins belongs to the exchange
                            (Default to [])
            __save_folder_path (str): Exchange's OS path to
                                      save coin files.
        """
        self.__coins = []

    @property
    def coins(self):
        """Possessed coins by exchange.

        Returns:
            list: cin object in exchange's coin list
        """
        return self.__coins

    @coins.setter
    def coins(self, data):
        if isinstance(data, list):
            self.__coins = data

    def possess_coin(self, coin):
        """Adds a coin obj to target exchange's coin list

        Args:
            coin (obj): new coin to posses
        """
        self.__coins.append(coin)

    def abandon_coin(self, coin):
        """Removes a coin from target exchange's coin list

        Args:
            coin (obj): coin to remove from stock
        """
        for i in self.__coins:
            if coin.name == i.name:
                self.__coins.remove(i)

    @ property
    @ abstractmethod
    def name(self) -> str:
        """Name of crypto-exchange.
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def website(self) -> str:
        """Website link of crypto-exchange.
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def api_website(self) -> str:
        """API Website link of crypto-exchange.
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def max_API_requests(self):
        r"""Maximum allowable number of API requests and period.

        Exchanges have request limits for a period or limited
        number of request. These limits must be defined by this
        variable. Default is 900 data per request.
        """
        raise NotImplementedError

    @ property
    def db_columns(self) -> list:
        """Provides database table columns and data types.
        """
        return [{'Column Name': 'Time',
                 'Data Type': 'DATETIME'},
                {'Column Name': 'HighPrice',
                 'Data Type': 'FLOAT(24)'},
                {'Column Name': 'LowPrice',
                 'Data Type': 'FLOAT(24)'},
                {'Column Name': 'OpenPrice',
                 'Data Type': 'FLOAT(24)'},
                {'Column Name': 'ClosePrice',
                 'Data Type': 'FLOAT(24)'},
                {'Column Name': 'Volume',
                 'Data Type': 'FLOAT(24)'}]

    @property
    def common_info(self) -> str:
        """Provides a common info for all exchanges.

        Returns:
            (str): general info for market data terms of use
        """
        return f'By accessing the {self.name.upper()} Market Data API, ' \
            'you agree to be bound by the Market Data Terms of Use! ' \
            'Please check its web site for more info...\n--------\n'\
            'Historical rate data can be sometimes incomplete! ' \
            'Exchanges do not always guarantee to provide data ' \
            'for intervals where there are no ticks.'

    @property
    def resolution(self):
        """Provides data download resolution of exchanges.

        Returns:
            (tuple): exchange specific API resolutions
        """
        return ('minutes',
                'hours',
                'days',
                'weeks',
                'months')

    def err_msg(self, msg) -> str:
        """Provides format of API connection error messages.

        Args:
            msg (str): error msg provided by exchange API

        Returns:
            str: error message  ready to be displayed in application
        """
        return f'An error was received from API of {self.name.upper()}:' \
            f'\n\n{msg}\n\n' \
            'You can find more info in below link:\n' \
            f'{self.api_website}'

    @ property
    @ abstractmethod
    def api_key(self) -> str:
        """API key of crypto exchange.
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def secret_key(self) -> str:
        """Secret key of crypto exchange.
        """
        raise NotImplementedError

    @ abstractmethod
    def connect_API(self):
        """If exists, create python library connection to exchange's API.
        """
        raise NotImplementedError

    @ abstractmethod
    def provide_available_coins(self):
        """Connects exchange's API and gets all available coins. 

        Returns:
            str: all available coins in the exchange
        """
        raise NotImplementedError

    @ abstractmethod
    def download_hist_data(self, symbol, start_date, end_date) -> list:
        """download_hist_data [summary]

        Args:
            symbol (str): Symbol of crypto asset
            start_date (str): start date of download request
            end_date (str): end date of download request

        Returns:
            list: downloaded historical data
        """

        raise NotImplementedError

    @ abstractmethod
    def correct_downloaded_data(self, downloaded_data) -> list:
        """Corrects & modifies downloaded data for SQL upload

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: corrected downloaded data for SQL upload
        """
        raise NotImplementedError
