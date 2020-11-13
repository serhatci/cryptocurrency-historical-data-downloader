"""Provides a class for creating coin objects.

    list of classes:
        Coin
    """
import arrow


class Coin:
    """Provides a coin obj for exchanges
    """

    def __init__(self, exc, data):
        """Constructor of Coin class

        Args:
            exc (obj) : exchange
            data (dict): data of target coin
        """
        self.name = data['Name']
        self.quote = data['Quote']
        self.base = data['Base']
        self.start_date = arrow.get(
            f"{data['StartDate']} {data['StartHour']}",
            'DD-MM-YYYY hh:mm:ss')
        self.end_date = arrow.get(
            f"{data['EndDate']} {data['EndHour']}",
            'DD-MM-YYYY hh:mm:ss')
        self.frequency = data['Frequency'].replace('\n', '')
        self.last_update = data['LastUpdate']
        self.file_name = '{}_{}_{}_{}_{}_{}.csv'.format(
            self.name,
            self.quote,
            self.base,
            self.frequency,
            exc.name,
            self.start_date.format('DD-MM-YYYY'))

    def __str__(self):
        """Provies readable representation of coin obj.

        Returns:
            str: readable representation of coin
        """
        return f'{self.name} object'
