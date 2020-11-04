"""Provides a class for creating coin objects.

    list of classes:
        Coin
    """


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
        self.abbr = data['Abbr']
        self.start_date = data['StartDate']
        self.start_hour = data['StartHour']
        self.end_date = data['EndDate']
        self.end_hour = data['EndHour']
        self.frequency = data['Frequency'].replace(' ', '-')
        self.file_name = '{}_{}_{}_{}.csv'.format(self.name,
                                                  exc.name,
                                                  self.frequency,
                                                  self.start_date)

    def __str__(self):
        """Provies readable representation of coin obj.

        Returns:
            str: readable representation of coin
        """
        return f'{self.name} object'