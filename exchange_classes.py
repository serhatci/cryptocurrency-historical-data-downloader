"""Provides classes of crypto exchanges.

List of Classes:
    Bitpanda
"""

import time
import arrow  # Date/time management library
import requests
from exchange_base_cls import Exchange


class Bitpanda(Exchange):
    """Creates bitpanda crypto-exchange object
    """

    name = 'Bitpanda'
    website = 'https://www.bitpanda.com/'
    hist_start_date = '2020-01-01 00:00:00+00:00'
    max_API_requests = [960, 'counts']
    block_time_check = True
    db_columns = [{'Colum Name': 'OpenDate',
                   'Data Type': 'DATETIMEOFFSET(0)'},
                  {'Colum Name': 'OpenDateMs',
                   'Data Type': 'BIGINT'},
                  {'Colum Name': 'OpenPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Colum Name': 'HighPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Colum Name': 'LowPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Colum Name': 'ClosePrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Colum Name': 'Volume',
                   'Data Type': 'FLOAT(24)'},
                  {'Colum Name': 'CloseDateMs',
                   'Data Type': 'BIGINT'},
                  {'Colum Name': 'TotalAmount',
                   'Data Type': 'FLOAT(24)'},
                  {'Colum Name': 'LastSequence',
                   'Data Type': 'BIGINT'}]
    time_col_index = 0
    api_key = None
    secret_key = None

    def connect_API(self) -> object:
        """Create connection to exchange API

        Returns:
            object: API connection object
        """
        pass

    def download_hist_data(self, symbol, start_date, end_date):
        """Downloads historical data of selected crypto asset

        Args:
            symbol (str): symbol of crypto asset
            start_date (str): data start date of request
            end_date (str): data end date of request
        """
        pass

    def correct_downloaded_data(self, downloaded_data) -> list:
        """Corrects % modify downloaded data for SQL upload.

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: data for SQL upload 
        """
        pass