"""Provides screen layout for the application.

List of Classes:
    Layout
"""
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Button   # GUI framework library


class Layout:
    """Provides a screen layout for the application.

    Screen layout design looks like below:

    |  col1 |              col2              |
    |       |                                |
    |       |--------------------------------|
    |       | col2_bot_left | col2_bot_right |
    |       |               |                |

    Returns:
        None
    """

    @classmethod
    def create(cls, exc_list, default_save_folder):
        """Creates screen layout.

        Args:
            exc_list (list): list of exchange objects

        Returns:
            list: Layout of two columns
        """
        # TanBlue theme is selected for this project
        sg.theme('TanBlue')

        return [[sg.Column(cls.__col1_layout(exc_list),
                           vertical_alignment='top'),
                 sg.Column(cls.__col2_layout(default_save_folder))]]

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
                          def_col_width=20,
                          auto_size_columns=False,
                          num_rows=table_rows,
                          enable_events=True,
                          bind_return_key=True,
                          key='-exchanges_table-')]]

    @classmethod
    def __col2_layout(cls, default_save_folder):
        """Creates layout of column2.

        Returns:
            list: layout of column2
        """

        return [[sg.Text('Select Cryptocurrency')],
                [sg.Table([['Bitcoin', 'BTC', '10/10/2020', '01/10/2020']],
                          headings=[' Cryptocurrency ',
                                    ' Abbreviation ',
                                    '      Last Update      ',
                                    '      Start Date       '],
                          justification='left',
                          row_height=30,
                          num_rows=5,
                          key='-coins_table-',
                          enable_events=True)],
                [sg.Column(cls.__col2_bot_left_layout(default_save_folder),
                           vertical_alignment='top'),
                 sg.Column(cls.__col2_bot_right_layout())]]

    @staticmethod
    def __col2_bot_left_layout(default_save_folder):
        """Creates layout of bottom left of column2.

        Returns:
            list: layout of bottom left of column2
        """

        frame1_layout = [[sg.Text('Coin Name:'),
                          sg.Input('', size=(34, 1),
                                   key='-coin_name-')],
                         [sg.Text('Coin Abbreviation:'),
                          sg.Input('', size=(29, 1),
                                   key='-abbr-')],
                         [sg.Text('Start Date:'),
                          sg.Text('01/01/2020',
                                  key='-start_date-',
                                  text_color="green"),
                          sg.Text('00:00:00',
                                  key='-start_hour-',
                                  text_color="green"),
                          sg.Text('UTC', key='-utc-',
                                  text_color="green"),
                          sg.CalendarButton('Calendar',
                                            target='-start_date-',
                                            pad=None,
                                            key='-calendar-',
                                            format=('%d-%m-%Y'))],
                         [sg.Button('ADD', key='-add_coin-')]]

        frame2_layout = [[sg.Text(default_save_folder,
                                  size=(40, 3),
                                  background_color='white',
                                  key='-folder-')],
                         [sg.Button('Change Folder',
                                    key='-change_folder-')]]

        return [[sg.Button('UPDATE COIN',
                           pad=((4, 14), (8, 1)),
                           size=(12, 1),
                           key='-update_coin-'),
                 sg.Button('UPDATE ALL',
                           pad=((0, 14), (8, 1)),
                           size=(12, 1),
                           button_color=('white', 'green'),
                           key='-update_all-'),
                 sg.Button('DELETE',
                           pad=((0, 0), (8, 1)),
                           size=(12, 1),
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
                                      size=(44, 15),
                                      autoscroll=True,
                                      disabled=True,
                                      key='-output_panel-')]]

        return [[sg.Frame('OUTPUT PANEL',
                          frame_layout,
                          title_color='green')]]
