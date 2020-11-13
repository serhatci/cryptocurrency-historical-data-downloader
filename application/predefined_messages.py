class PredefinedMessages:
    """Contains pre-defined messages.

    Class Attr:
        __messages [dict]: dictionary of pre-defined messages
                           which controller can select among them
    """
    _messages = {
        '*Select Exchange':
            'Please select an exchange first!',
        '*Select Coin':
            'Please select a cryptoasset first!',
        '*No Coin':
            'Exchange has no cryptoasset yet!',
        '*Empty':
            'Please fill below mentioned inputs!',
        '*Folder Changed':
            'Save folder path has been changed successfully!',
        '*Coin Added':
            'A new cryptoasset has been added successfully:',
        '*Coin Exist':
            'Cryptoasset you are trying to add is already existed!',
        '*Corrupted Coin':
            'Data file of below cryptoasset could not be found '
            'in saving folder!',
        '*Coin Deleted':
            'Below cryptoasset has been deleted:',
        '*Progress':
            'Data downloaded successfully and saved to coin file '
            'for below dates:',
        '*Cancelled':
            '-- Download INTERRUPTED! --\n\n'
            'You can delete data file if you do not need it anymore...',
        '*Down Start':
            'Historical data will be downloaded in total of:',
        '*Already Downloaded':
            'Historical data of selected cryptoasset has already '
            'been downloaded! \nYou can use UPDATE button if you are '
            'willing to update data to current time...',
        '*Already Update':
            'Historical data of selected cryptoasset is already up to date!',
        '*Name Err':
            'Coin name can not be empty and must include only numbers or '
            'letters in ENGLISH Alphabet!',
        '*Quote-Base Err':
            'Base or Quote coin should be an abbreviation such as '
            'USD, EUR, GBP or BTC, ETH, XRP etc.\n\n'
            'Abbreviations can differ from exchange to exchange. '
            'Please be sure you use right abbreviation for the relevant '
            'exchange!',
        '*Format Err':
            'Input format of DATE or HOUR is wrong!\n\nDate and hour '
            'should be given in this format:\n01-01-2020 23:00:00',
        '*Date Err':
            'Start date can not be later than end date!'
    }
