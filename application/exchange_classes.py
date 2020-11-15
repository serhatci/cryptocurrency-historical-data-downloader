"""Provides classes of crypto exchanges.

List of Classes:
    Bitpanda
"""

import arrow
import requests
from exchange_base_cls import Exchange


class Bitpanda(Exchange):
    """Creates bitpanda crypto-exchange object
    """

    name = 'Bitpanda'
    website = 'https://www.bitpanda.com/'
    hist_start_date = '2020-01-01 00:00:00+00:00'
    max_API_requests = 900
    block_time_check = True
    db_columns = [{'Column Name': 'HighPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'LowPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'OpenPrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'ClosePrice',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'TotalAmount',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'Volume',
                   'Data Type': 'FLOAT(24)'},
                  {'Column Name': 'Time',
                   'Data Type': 'DATETIME'}]
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
                  'You can find more info in below link:\n' \
                  'https://developers.bitpanda.com/exchange/?python'
            raise ConnectionError(msg)
        else:
            return self.correct_downloaded_data(data.json())

    def correct_downloaded_data(self, downloaded_data):
        """Corrects & modifies downloaded data for cvs file.

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: data for csv file save
        """
        return [[arrow.get(data['time']).format('YYYY-MM-DD HH:mm:ss'),
                 data['high'],
                 data['low'],
                 data['open'],
                 data['close'],
                 data['total_amount'],
                 data['volume']] for data in downloaded_data]


class Exmo(Exchange):
    """Creates Exmo crypto-exchange object
    """

    name = 'Exmo'
    website = 'https://www.exmo.com'
    hist_start_date = '2020-01-01 00:00:00+00:00'
    max_API_requests = 900
    block_time_check = True
    db_columns = [{'Column Name': 'Time',
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
        try:
            data = requests.get('https://api.exmo.com/v1.1/currency')
            return str(data.json()).strip('[]')
        except ConnectionError as err:
            return '\nProblem occurred while connecting to API of '
            f'{self.name.upper()}\n\n{err}'

    def download_hist_data(self, coin, time):
        """Downloads historical data of selected crypto asset.

        Args:
            coin (obj): given coin
            time (list): [start date obj,end date obj]
        """
        def res(freq):
            if freq == 'minutes':
                return '1'
            if freq == 'hours':
                return '60'
            if freq == 'days':
                return 'D'
            if freq == 'weeks':
                return 'W'
            if freq == 'months':
                return 'M'

        data = requests.get('https://api.exmo.com/v1.1/candles_history', {
            'symbol': f'{coin.quote}_{coin.base}',
            'resolution': res(coin.frequency),
            'from': time[0].timestamp,
            'to': time[1].timestamp
        })
        try:
            return self.correct_downloaded_data(data.json()['candles'])
        except:
            msg = f'An error was received from API of {self.name.upper()}:' \
                  f'\n\n{data.json()}\n\n' \
                  'You can find more info in below link:\n' \
                  'https://documenter.getpostman.com/view/10287440/SzYXWKPi'
            raise ConnectionError(msg)

    def correct_downloaded_data(self, downloaded_data):
        """Corrects & modifies downloaded data for cvs file.

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: data for csv file save
        """
        return [[arrow.get(int(data['t'])).format('YYYY-MM-DD HH:mm:ss'),
                 data['h'],
                 data['l'],
                 data['o'],
                 data['c'],
                 data['v']]
                for data in downloaded_data]
