import os
import arrow
import pandas as pd
from coin_cls import Coin


def get_coin_files(exc, save_path):
    """Provides all coin file paths in a given exchange's folder.

    Args:
        exc (obj): target exchange
        save_path (str): main save path in OS

    Returns:
        (list): filtered coin file paths from all
                files existed in the exchange folder
    """
    exc_path = os.path.join(save_path, exc.name)
    if not os.path.isdir(exc_path):
        return []
    else:
        all_files = os.listdir(exc_path)
        coin_files = list(filter(lambda x:
                                 x.count('_') == 5 and
                                 x.count('-') == 2 and
                                 x.find('.csv'), all_files))
        return [os.path.join(exc_path, file) for file in coin_files]


def create_exc_folder(exc, save_path):
    """Creates a directory of exchange in the OS.

    Args:
        exc (str): target exchange
        save_path (str): main save path in OS
    """
    exc_path = os.path.join(save_path, exc.name)
    if not os.path.isdir(exc_path):
        os.mkdir(exc_path)


def read_last_update_from_file(file_path):
    """Reads last date of data downloaded from cin file.

    Args:
        file_path (str): path of coin file

    Returns:
        (obj): last date of coin data
    """
    with open(file_path) as f:
        data = f.readlines()
        if len(data) > 4:
            return arrow.get(data[-1].split(';')[-1])


def form_new_coin_data(comment, last_update):
    """Forms a coin data dictionary from existing file.

    Args:
        data (str): coin data collected from comment in coin file
        last_update (list) : latest date and hour received from 
                             downloaded coin data

    Raises:
        ValueError: occurs if info comment read from coin file is
                    in different format than expected

    Returns:
        coin_data (dict): coin data for object creation
    """
    data = comment.split(' ')
    if not len(data) == 8:
        raise ValueError(
            f'Csv file of {data[0]} found in the exchanage folder.\n'
            'However the file name was not in correct format!\n\n')
    return {'Name': data[0],
            'Quote': data[1],
            'Base': data[2],
            'StartDate': data[3],
            'StartHour': data[4],
            'EndDate': data[5],
            'EndHour': data[6],
            'Frequency': data[7],
            'LastUpdate': last_update}


def read_file_comment(file_path):
    """Reads info comment in a coin file.

    Args:
        file_path (str): given coin file path

    Raises:
        ValueError: occurs if no comment exist at the top
                    of coin file

    Returns:
        comment (str): info comment in the coin file 
    """
    with open(file_path, 'r') as f:
        line = f.readline()
        if not line.startswith('#'):
            raise ValueError(
                f'{file_path} does not starts with info comment!\n\n')
        return line.replace('#', '')


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
        write_initial_comment(coin, file_path)
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, index=False, sep=';', mode='a')
    else:
        raise FileExistsError(
            f'{coin.name.upper()} already exists in the system:'
            f'\n{file_path}')


def write_initial_comment(coin, file_path):
    """Creates an info comment for given coin and writes it in coin file.

    Args:
        coin (obj): target coin
        file_path (str): coin file path in OS
    """
    comment = '#{} {} {} {} {} {}'.format(
        coin.name,
        coin.quote,
        coin.base,
        coin.start_date.format('DD-MM-YYYY hh:mm:ss'),
        coin.end_date.format('DD-MM-YYYY hh:mm:ss'),
        coin.frequency)
    line = '\n#-----------------------------------------------------------'
    with open(file_path, 'w') as f:
        f.write(comment+line)


def delete_exc_folder(exc, save_path):
    """Deletes given exchange's folder from OS.

    Args:
        exc (obj): target exchange
        save_path (str): main save path in OS
    """
    exc_path = os.path.join(save_path, exc.name)
    os.rmdir(exc_path)


def delete_coin_file(exc, coin, save_path):
    """Deletes given coin's csv file from OS.

    Args:
        exc (obj): exchange possessing coin
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
        coin_data (list): data of coin

    Returns:
        obj: new coin
    """
    return Coin(exc, coin_data)


def save_data(exc, coin, data, save_path):
    """Saves downloaded date to coin csv file.

    Args:
        exc (obj): exchange possessing coin
        coin (obj) : target coin
        data (list): downloaded coin data
        save_path (str): main save path
    """
    exc_path = os.path.join(save_path, exc.name)
    file_path = os.path.join(exc_path, coin.file_name)
    df = pd.DataFrame(data)
    df.to_csv(file_path, header=False, index=False, sep=';', mode='a')
