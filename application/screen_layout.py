"""Provides screen layout for the application.

List of Classes:
    Layout
"""
import PySimpleGUI as sg  # GUI framework library


class Layout:
    """Provides a PYsimpleGUI screen layout for the application.

    Screen layout design looks like below:

    |  col1 |              col2              |
    |       |                                |
    |       |--------------------------------|
    |       | col2_bot_left | col2_bot_right |
    |       |               |                |

    see below for more info:
    https://pysimplegui.readthedocs.io/en/latest/

    Returns:
        None
    """

    @classmethod
    def create(cls, exc_list, save_folder, start_date,
               start_hour, end_date, end_hour):
        """Creates screen layout.

        Args:
            exc_list (list): list of exchange objects
            save_folder (str): default path of save folder
            start_date (str): default start date
            start_hour (str): default start hour
            end_date (str): default end date
            end_hour (str): default end hour

        Returns:
            list: screen Layout
        """
        # TanBlue theme is selected for this project
        sg.theme('TanBlue')

        return [[sg.Column(cls.__col1_layout(exc_list),
                           vertical_alignment='top'),
                 sg.Column(cls.__col2_layout(save_folder,
                                             start_date,
                                             start_hour,
                                             end_date,
                                             end_hour))]]

    @staticmethod
    def __col1_layout(exc_list):
        """Creates layout of colum1.

        Args:
            exc_list (list): list of exchange objects

        Returns:
            list: layout of column1
        """

        # table variables
        table_headings = ['Exchange Name']
        table_values = [[exc.name] for exc in exc_list]
        table_rows = len(exc_list)

        return [[sg.Text('Select Crypto Exchange')],
                [sg.Table(table_values,
                          headings=table_headings,
                          justification='left',
                          background_color='white',
                          row_height=30,
                          def_col_width=14,
                          auto_size_columns=False,
                          num_rows=table_rows,
                          enable_events=True,
                          bind_return_key=True,
                          key='-exchanges_table-')]]

    @classmethod
    def __col2_layout(cls, save_folder, start_date, start_hour,
                      end_date, end_hour):
        """Creates layout of column2.

        Returns:
            list: layout of column2
        """

        return [[sg.Text('Select Cryptocurrency')],
                [sg.Table([['', '', '', '', '']],
                          headings=[' Cryptocurrency ',
                                    ' Trade Pair ',
                                    '    Last Update      ',
                                    '     Start Date      ',
                                    '   Frequency   '],
                          justification='center',
                          row_height=30,
                          num_rows=5,
                          key='-coins_table-',
                          enable_events=True,
                          background_color='white',
                          text_color='Black')],
                [sg.Column(cls.__col2_bot_left_layout(save_folder,
                                                      start_date,
                                                      start_hour,
                                                      end_date,
                                                      end_hour),
                           vertical_alignment='top'),
                 sg.Column(cls.__col2_bot_right_layout())]]

    @staticmethod
    def __col2_bot_left_layout(save_folder, start_date, start_hour,
                               end_date, end_hour):
        """Creates layout of bottom left of column2.

        Returns:
            list: layout of bottom left of column2
        """

        frame1_layout = [[sg.Text('Coin Name:'),
                          sg.Input('', size=(26, 1),
                                   key='-coin_name-'),
                          sg.Button(' AVAILABLE COINS? ',
                                    key='-available_coins-')],
                         [sg.Text('Quote Coin:'),
                          sg.Input('BTC, ETH etc...', size=(17, 1),
                                   key='-quote-'),
                          sg.Text('Base Coin:'),
                          sg.Input('USD, EUR etc...', size=(17, 1),
                                   key='-base-')],
                         [sg.Text('Start Date: '),
                          sg.Input(start_date,
                                   key='-start_date-',
                                   size=(10, 1)),
                          sg.Input(start_hour,
                                   key='-start_hour-',
                                   size=(8, 1)),
                          sg.Text('UTC', text_color='green'),
                          sg.CalendarButton('Calendar',
                                            target='-start_date-',
                                            pad=None,
                                            key='-calendar-',
                                            format=('%d-%m-%Y'))],
                         [sg.Text('End  Date: '),
                          sg.Input(end_date,
                                   key='-end_date-',
                                   size=(10, 1)),
                          sg.Input(end_hour,
                                   key='-end_hour-',
                                   size=(8, 1)),
                          sg.Text('UTC', text_color='green'),
                          sg.CalendarButton('Calendar',
                                            target='-end_date-',
                                            pad=None,
                                            key='-calendar-',
                                            format=('%d-%m-%Y'))],
                         [sg.Text('Frequency/Resolution/Granularity: '),
                          sg.InputCombo(('minutes',
                                         'hours',
                                         'days',
                                         'weeks',
                                         'months'),
                                        default_value='minutes',
                                        key='-frequency_input-',
                                        size=(15, 1))],
                         [sg.Button('   ADD   ', key='-add_coin-')]]

        frame2_layout = [[sg.Text(save_folder,
                                  size=(52, 2),
                                  background_color='white',
                                  key='-folder-')],
                         [sg.Button('Change Folder',
                                    key='-change_folder-')]]

        return [[sg.Button('DOWNLOAD',
                           pad=((4, 8), (8, 1)),
                           size=(12, 1),
                           key='-download_coin-'),
                 sg.Button('UPDATE',
                           pad=((0, 8), (8, 1)),
                           size=(8, 1),
                           key='-update_coin-'),
                 sg.Button('CANCEL',
                           pad=((0, 55), (8, 1)),
                           size=(8, 1),
                           button_color=('white', 'orange'),
                           key='-cancel-'),
                 sg.Button('DELETE COIN',
                           pad=((0, 0), (8, 1)),
                           size=(14, 1),
                           button_color=('white', 'red'),
                           key='-delete_coin-')],
                [sg.Frame('ADD NEW COIN',
                          frame1_layout,
                          title_color='green')],
                [sg.Frame('SAVE FOLDER',
                          frame2_layout,
                          title_color='green')]]

    @ staticmethod
    def __col2_bot_right_layout():
        """Creates layout of bottom right of column2.

        Returns:
            list: layout of bottom right of column2
        """

        frame_layout = [[sg.Multiline(default_text='',
                                      size=(42, 18),
                                      autoscroll=True,
                                      disabled=True,
                                      key='-output_panel-',
                                      pad=(2, 2),
                                      auto_refresh=True)]]

        return [[sg.Frame('OUTPUT PANEL',
                          frame_layout,
                          title_color='green')]]
