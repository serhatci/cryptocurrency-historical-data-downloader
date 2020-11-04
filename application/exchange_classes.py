"""Provides classes of crypto exchanges.

List of Classes:
    Bitpanda
"""

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
            str: all available coin in the exchange
        """
        headers = {'Accept': 'application/json'}
        try:
            r = requests.get(
                'https://api.exchange.bitpanda.com/public/v1/currencies',
                headers=headers)
        except Exception as err:
            return '\nProblem occurred while connecting to API of ' \
                   f'{self.name.upper()}\n\n{err}'
        else:
            return str([coin['code'] for coin in r.json()]).strip('[]')

    @staticmethod
    def download_hist_data(symbol, unit, period, start_date, end_date):
        """Downloads historical data of selected crypto asset.

        Args:
            symbol (str): symbol of crypto asset
            unit (str): MINUTES, HOURS, DAYS etc...
            period (int): number of units
            start_date (str): data start date of request
            end_date (str): data end date of request
        """
        link = 'https://api.exchange.bitpanda.com/' \
               'public/v1/candlesticks/{}'.format(symbol)

        headers = {'Accept': 'application/json'}

        # try:
        r = requests.get(link,
                         params={'unit': unit.upper(),
                                 'period': period,
                                 'from': start_date,
                                 'to': end_date},
                         headers=headers)
        # except Exception as err:
        #     print(err)
        #     return err
        # else:
        return r.json()

    def correct_downloaded_data(self, downloaded_data) -> list:
        """Corrects % modify downloaded data for SQL upload.

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: data for SQL upload 
        """
        pass
