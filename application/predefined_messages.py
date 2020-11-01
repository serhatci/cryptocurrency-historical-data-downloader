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
            'Please select a coin first!',
        '*No Coin':
            'Exchange has no coin yet!',
        '*Missing Name':
            'Please fill Coin Name input!',
        '*Missing Abbr':
            'Please fill Coin Abbreviation input!',
        '*Folder Changed':
            'Saving folder has been changed successfully.\n\n'
            'If you have downloaded coin files in previous folder'
            'they will not be visible in this folder!..',
        '*Coin Added':
            'A new cryptoasset has been added successfully.',
        '*Coin Exist':
            'Coin you are trying to add is already existed!',
        '*Corrupted Coin':
            'Data file of below coins could not be found in saving folder!',
        '*Coin Deleted':
            'Selected cryptoassethas been deleted successfully.'
    }
