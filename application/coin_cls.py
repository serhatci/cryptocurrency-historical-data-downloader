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
        self.file_name = '{}_{}_{}.csv'.format(self.name,
                                               exc.name,
                                               self.start_date)

    def __str__(self):
        """Provies readable representation of coin obj.

        Returns:
            str: readable representation of coin
        """
        return f'{self.name} object'
