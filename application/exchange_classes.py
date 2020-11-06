"""Provides classes of crypto exchanges.

List of Classes:
    Bitpanda
"""

import requests
import arrow
import json
from exchange_base_cls import Exchange


class Bitpanda(Exchange):
    """Creates bitpanda crypto-exchange object
    """

    name = 'Bitpanda'
    website = 'https://www.bitpanda.com/'
    hist_start_date = '2020-01-01 00:00:00+00:00'
    max_API_requests = 960
    block_time_check = True
    db_columns = [{'Column Name': 'OpenDate',
                   'Data Type': 'DATETIMEOFFSET(0)'},
                  {'Column Name': 'OpenDateMs',
                   'Data Type': 'BIGINT'},
                  {'Column Name': 'OpenPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'HighPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'LowPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'ClosePrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'Volume',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'CloseDateMs',
                   'Data Type': 'BIGINT'},
                  {'Column Name': 'TotalAmount',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'LastSequence',
                   'Data Type': 'BIGINT'}]
    time_col_index = 0
    api_key = None
    secret_key = None

    def connect_API(self) -> None:
        """Create connection to exchange API

        Returns:
            object: API connection object
        """
        pass

    def provide_available_coins(self):
        """Connect exchange's API and gets all available coins. 

        Returns:
            str: all available coins in the exchange
        """
        headers = {'Accept': 'application/json'}
        try:
            r = requests.get(
                'https://api.exchange.bitpanda.com/public/v1/currencies',
                headers=headers)
        except ConnectionError as err:
            return '\nProblem occurred while connecting to API of ' \
                   f'{self.name.upper()}\n\n{err}'
        else:
            return str([coin['code'] for coin in r.json()]).strip('[]')

    def download_hist_data(self, coin, time):
        """Downloads historical data of selected crypto asset.

        Args:
            coin (obj): given coin
            time (list): [start date obj,end date obj]
        """
        link = f'https://api.exchange.bitpanda.com/' \
               f'public/v1/candlesticks/{coin.quote}_{coin.base}'
        headers = {'Accept': 'application/json'}
        data = requests.get(link,
                            params={'unit': coin.frequency.upper(),
                                    'period': '1',
                                    'from': time[0],
                                    'to': time[1]},
                            headers=headers)
        if not data.status_code == 200:
            msg = f'An error was received from API of {self.name.upper()}:' \
                  f'\n\n{data.text}\n\n' \
                'You can find more info in below link:' \
                  f'\nhttps://developers.bitpanda.com/exchange/?python'
            raise ConnectionError(msg)
        else:
            return data.json()

    def correct_downloaded_data(self, downloaded_data) -> list:
        """Corrects % modify downloaded data for SQL upload.

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: data for SQL upload 
        """
        pass
