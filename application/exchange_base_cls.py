"""Provides a base class for creating crypto-exchange classes.

    List of classes:
        Exchange
        Coin
    """
from abc import ABC, abstractmethod
from tkinter.constants import SEL


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
    def hist_start_date(self) -> str:
        """Start date of historical data.

        It defines the oldest date in the historical data
        which will be downloaded. It must be UTC date time.

        Example '2020-01-01 00:00:00+00:00'
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def max_API_requests(self):
        r"""Maximum allowable number of API requests and period.

        Exchanges have request limits for a period or limited
        number of request. These limits must be defined by this
        variable in a list with predefined format such as
        [limit number,'minutes/days/weeks/counts']

        Example [4,'weeks']
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def block_time_check(self) -> bool:
        """Defines if block time check is required.

        Some exchanges allow historical data download only
        by defined periods. In this situations, several
        request should be made with time blocks instead
        downloading whole historical data by a single request
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def db_columns(self) -> list:
        """Defines SQL table columns and data types.

        Each crypto exchange provides historical data in
        different format. Column names and SQL data types
        must be predefined to create SQL tables.

        Example: [{'Column Name': 'OpenDateMs', 'Data Type': 'BIGINT'}]
        """
        raise NotImplementedError

    @ property
    @ abstractmethod
    def time_col_index(self) -> int:
        """Index number of time column in downloaded data

        Index of time column is different in each crypto
        exchnage's provided historical data. I should be
        predefined to create consistent SQL tables for each
        crypto exchange.
        """
        raise NotImplementedError

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
        """Create connection to API of exchange.
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
