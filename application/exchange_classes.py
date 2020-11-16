"""Provides classes of crypto exchanges.

List of Classes:
    Bitpanda
    Exmo
    Coinbasepro
    Bitfinex
"""

import arrow
import requests
from exchange_base_cls import Exchange


class Bitpanda(Exchange):
    """Creates bitpanda crypto-exchange object
    """

    name = 'Bitpanda'
    website = 'https://www.bitpanda.com/'
    api_website = 'https://developers.bitpanda.com/exchange/?python'
    max_API_requests = 900
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
            data = requests.get(
                'https://api.exchange.bitpanda.com/public/v1/currencies',
                headers=headers)
            return str([coin['code'] for coin in data.json()]).strip('[]')
        except ConnectionError as err:
            return '\nProblem occurred while connecting to API of ' \
                   f'{self.name.upper()}\n\n{err}'

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
            raise ConnectionError(self.err_msg(data.text))
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
                 data['volume']] for data in downloaded_data]


class Exmo(Exchange):
    """Creates Exmo crypto-exchange object
    """

    name = 'Exmo'
    website = 'https://www.exmo.com'
    api_website = 'https://documenter.getpostman.com/view/10287440/SzYXWKPi'
    max_API_requests = 900
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
        data = requests.get('https://api.exmo.com/v1.1/candles_history', {
            'symbol': f'{coin.quote}_{coin.base}',
            'resolution': self.__resolution(coin.frequency),
            'from': time[0].timestamp,
            'to': time[1].timestamp
        })
        try:
            return self.correct_downloaded_data(data.json()['candles'])
        except:
            raise ConnectionError(self.err_msg(data.text))

    @ staticmethod
    def __resolution(freq):
        """Provides exchange specific resolution.

        Args:
            freq (str): frequency given by user

        Returns:
            str: appropriate resolution
        """
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


class Coinbasepro(Exchange):
    """Creates CoinbasePro crypto-exchange object
    """

    name = 'CoinbasePro'
    website = 'https://www.coinbase.com/'
    api_website = 'https://docs.pro.coinbase.com/#requests'
    max_API_requests = 250
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
            r = requests.get(
                'https://api.pro.coinbase.com/products')
            return str([coin['id'] for coin in r.json()]).strip('[]')
        except ConnectionError as err:
            return '\nProblem occurred while connecting to API of '
            f'{self.name.upper()}\n\n{err}'

    def download_hist_data(self, coin, time):
        """Downloads historical data of selected crypto asset.

        Args:
            coin (obj): given coin
            time (list): [start date obj,end date obj]
        """

        link = f'https://api.pro.coinbase.com/products/'
        f'{coin.quote}-{coin.base}/candles'
        data = requests.get(link, {
            'start': time[0].shift(seconds=int(self.__gran(coin.frequency))),
            'end': time[1],
            'granularity': self.__gran(coin.frequency),
        })
        if not data.status_code == 200:
            raise ConnectionError(self.err_msg(data.text))
        else:
            return self.correct_downloaded_data(data.json())

    @ staticmethod
    def __gran(freq):
        """Provides exchange specific granularity.

        Args:
            freq (str): frequency given by user

        Returns:
            str: appropriate granularity
        """
        if freq == 'minutes':
            return '60'
        if freq == 'hours':
            return '3600'
        if freq == 'days':
            return '86400'
        if freq == 'weeks':
            return '604800'
        if freq == 'months':
            return '2419200'

    def correct_downloaded_data(self, downloaded_data):
        """Corrects & modifies downloaded data for cvs file.

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: data for csv file save
        """
        return [[arrow.get(data[0]).format('YYYY-MM-DD HH:mm:ss'),
                 data[2],
                 data[1],
                 data[3],
                 data[4],
                 data[5]] for data in reversed(downloaded_data)]


class Bitfinex(Exchange):
    """Creates Bitfinex crypto-exchange object
    """

    name = 'Bitfinex'
    website = 'https://www.bitfinex.com'
    api_website = 'https://docs.bitfinex.com/docs/rest-general'
    max_API_requests = 10
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
            r = requests.get(
                'https://api-pub.bitfinex.com/v2/tickers?symbols=ALL')
            return str([coin[0] for coin in r.json()]).strip('[]')
        except ConnectionError as err:
            return '\nProblem occurred while connecting to API of '
            f'{self.name.upper()}\n\n{err}'

    def download_hist_data(self, coin, time):
        """Downloads historical data of selected crypto asset.

        Args:
            coin (obj): given coin
            time (list): [start date obj,end date obj]
        """
        link = f'https://api-pub.bitfinex.com/v2/candles/trade' \
            f':{self.__gran(coin.frequency)}'\
            f':t{coin.quote}{coin.base}/hist'
        data = requests.get(link, params={
            'limit': 10,
            'start': time[0].format("x")[:13],  # convert to ms
            'end': time[1].format("x")[:13],  # convert to ms
            'sort': '-1'})
        if not data.status_code == 200:
            raise ConnectionError(self.err_msg(data.text))
        else:
            return self.correct_downloaded_data(data.json())

    @ staticmethod
    def __gran(freq):
        """Provides exchange specific granularity.

        Args:
            freq (str): frequency given by user

        Returns:
            str: appropriate granularity
        """
        if freq == 'minutes':
            return '1m'
        if freq == 'hours':
            return '1h'
        if freq == 'days':
            return '1D'
        if freq == 'weeks':
            return '7D'
        if freq == 'months':
            return '1M'

    def correct_downloaded_data(self, downloaded_data):
        """Corrects & modifies downloaded data for cvs file.

        Args:
            downloaded_data (list): downloaded historical data

        Returns:
            list: data for csv file save
        """
        return [[arrow.get(data[0]).format('YYYY-MM-DD HH:mm:ss'),
                 data[3],
                 data[4],
                 data[1],
                 data[2],
                 data[5]] for data in reversed(downloaded_data)]
