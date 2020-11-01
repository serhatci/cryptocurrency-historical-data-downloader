import os
import pandas as pd
from coin_cls import Coin


def get_coin_files(exc, save_path):
    """Provides all coin files in a given exchange's folder.

    Args:
        exc_name (str): name of target exchange
        save_path (str): main save path in OS

    Returns:
        (list): filtered coin files from all
                files existed in the exchange folder
    """
    exc_path = os.path.join(save_path, exc.name)
    if not os.path.isdir(exc_path):
        return []
    else:
        all_files = os.listdir(exc_path)
        return list(filter(lambda x:
                           x.count('_') == 2 and
                           x.count('-') == 2 and
                           x.find('.csv'), all_files))


def create_exc_folder(exc, save_path):
    """Creates a directory of exchange in the OS.

    Args:
        exc_name (str): name of target exchange
        save_path (str): main save path in OS
    """
    exc_path = os.path.join(save_path, exc.name)
    if not os.path.isdir(exc_path):
        os.mkdir(exc_path)


def remove_missing_coins(exc, files):
    """Remove coins from system if they don't exist in OS.

    Args:
        exc (obj): target exchange
        files (list): coin files found in target exchange's folder

    Return:
        (list) : coin names removed from system
    """
    missing_coins = []
    coin_names = [file.split('_')[0] for file in files]
    for coin in exc.coins:
        if not coin.name in coin_names:
            missing_coins.append(coin)
    for coin in missing_coins:
        exc.abandon_coin(coin)
    return [coin.name for coin in missing_coins]


def add_new_found_coins(exc, files):
    """Add new coins to system if their file exist in OS.

    Args:
        exc (obj): target exchange
        files (list): coin files found in target exchange's folder
    """
    coin_names = [coin.name for coin in exc.coins]
    for file in files:
        if not file.split('_')[0] in coin_names:
            pass


def create_coin_file(exc, coin, save_path):
    """Creates a cvs file for a given coin.

    Args:
        exc (obj): exchange which coin belongs
        coin (obj): target coin
        save_path (str): main save path in OS
        """
    headers = [i['Column Name'] for i in exc.db_columns]
    exc_path = os.path.join(save_path, exc.name)
    file_path = os.path.join(exc_path, coin.file_name)
    if not os.path.isfile(file_path):
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, index=False, sep=';')
    else:
        raise FileExistsError(
            f'{coin.name} already exists in the system'
            f'\n--{file_path}--'
        )


def delete_exc_folder(exc, save_path):
    """Deletes given exchange's folder from OS.

    Args:
        exc_name (str): name of target exchange
        save_path (str): main save path in OS
    """
    exc_path = os.path.join(save_path, exc.name)
    os.rmdir(exc_path)


def delete_coin_file(exc, coin, save_path):
    """Deletes given coin's csv file from OS.

    Args:
        exc_name (str): name of exchange possessing coin 
        coin (obj) : target coin
        save_path (str): main save path in OS
    """
    exc_path = os.path.join(save_path, exc.name)
    file_path = os.path.join(exc_path, coin.file_name)
    os.remove(file_path)


def create_coin_obj(exc, coin_data):
    """Creates a coin obj from coin data

    Args:
        exc (obj): exchange possessing coin
        coin_data (dict): [description]

    Returns:
        obj: new coin
    """
    return Coin(exc, coin_data)
