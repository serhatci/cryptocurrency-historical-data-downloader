import os
import pandas as pd
from coin_cls import Coin


def get_coin_files(exc, save_path):
    """Provides all coin file paths in a given exchange's folder.

    Args:
        exc_name (str): name of target exchange
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
                                 x.count('_') == 2 and
                                 x.count('-') == 2 and
                                 x.find('.csv'), all_files))
        return [os.path.join(exc_path, file) for file in coin_files]


def create_exc_folder(exc, save_path):
    """Creates a directory of exchange in the OS.

    Args:
        exc_name (str): name of target exchange
        save_path (str): main save path in OS
    """
    exc_path = os.path.join(save_path, exc.name)
    if not os.path.isdir(exc_path):
        os.mkdir(exc_path)


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
                f'{file_path} does not starts with info comment!')
        return line.replace('#', '')


def form_new_coin_data(comment):
    """Forms a coin data dictionary from given comment.

    Args:
        comment (str): info comment read from coin file

    Raises:
        ValueError: occurs if info comment is in different
                    format than expected

    Returns:
        coin_data (dict): coin data for object creation
    """
    data = comment.split(' ')
    if not len(data) == 6:
        raise ValueError(
            f'{comment} does not represent correct coin info!')
    return {'Name': data[0],
            'Abbr': data[1],
            'StartDate': data[2],
            'StartHour': data[3],
            'EndDate': data[4],
            'EndHour': data[5]}


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
            f'\n{coin.name} already exists in the system'
            f'\n\n--{file_path}--\n'
        )


def write_initial_comment(coin, file_path):
    """Creates an info comment for given coin and writes it in coin file.

    Args:
        coin ([type]): [description]
        file_path ([type]): [description]
    """
    comment = '#{} {} {} {} {} {}'.format(coin.name,
                                          coin.abbr,
                                          coin.start_date,
                                          coin.start_hour,
                                          coin.end_date,
                                          coin.end_hour)
    line = '\n#-----------------------------------------\n'
    with open(file_path, 'w') as f:
        f.write(comment+line)


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
        coin_data (list): data of coin

    Returns:
        obj: new coin
    """
    return Coin(exc, coin_data)
