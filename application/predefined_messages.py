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
        '*Missing Name':
            'Please fill Coin Name input!',
        '*Missing Quote':
            'Please fill Quote Coin input!',
        '*Missing Base':
            'Please fill Base Coin input!',
        '*Folder Changed':
            'Save folder path has been changed successfully!',
        '*Coin Added':
            'A new cryptoasset has been added successfully:',
        '*Coin Exist':
            'Cryptoasset you are trying to add is already existed!',
        '*Corrupted Coin':
            'Data file of below cryptoasset could not be found in saving folder!',
        '*Coin Deleted':
            'Below cryptoasset has been deleted successfully:',
        '*Progress':
            'Data downloaded successfully and saved to coin file for below dates:',
        '*Cancelled':
            'Download was CANCELLED!\n\nRelevant cryptoasset file was deleted!...',
        '*Down Start':
            'Historical data will be downloaded in total of:',
    }
