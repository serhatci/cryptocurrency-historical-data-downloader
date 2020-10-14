import PySimpleGUI as sg  # GUI framework library
from screen_layout import Layout
from model_view_controller import Controller, Model, View
from exchange_base_cls import Exchange
from exchange_classes import *


def run():
    """Executes the application.
    """
    # instantiate application object
    app = Controller(Model(), View())

    # Instantiate all exchange classes defined in exchange_classes.py
    exc_list = [cls() for cls in Exchange.__subclasses__()]

    # Get savefolder location
    default_save_folder = app.get_default_folder()

    # Creates the start screen layout
    layout = Layout.create(exc_list, default_save_folder)

    # Initializes start screen and attaches it to app.view object
    app.view.window = sg.Window('Crypto-exchanges Data Downloader',
                                layout,
                                size=(1000, 500),
                                finalize=True)

    # Initial states of user selections
    selected_exc = None
    selected_coin = None

    # Listens the screen and collects user inputs
    while True:
        event, values = app.view.window.read()

        # Terminate app when user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        # Displays coins belong to the selected exchange
        # Displays exchange info when it is clicked
        if event == '-exchanges_table-':
            col_num = values['-exchanges_table-'][0]
            selected_exc = exc_list[col_num]
            app.update_coin_tbl(selected_exc)
            selected_exc.coins = app.view.window['-coins_table-'].Get()
            msg = f'{selected_exc.name}\n-----\n' \
                f'{selected_exc.website}'
            app.display(msg, 'green')

        if event == '-coins_table-':
            if not selected_exc:
                app.display('*Select Exchange')
            else:
                col_num = values['-coins_table-'][0]
                selected_coin = selected_exc.coins[col_num]

        # User clicks -add- button and a new coin is added
        if event == '-add_coin-':
            if not selected_exc:
                app.display('*Select Exchange')
            else:
                if (
                    values['-coin_name-'] == '' or
                    values['-abbr-'] == '' or
                    app.view.window['-folder-'].get() == 'C:\..'
                ):
                    app.display('*Missing Info')
                else:
                    coin_name = values['-coin_name-']
                    abbr = values['-abbr-']
                    start_date = app.view.window['-start_date-'].get()
                    start_hour = app.view.window['-start_hour-'].get()
                    save_folder = app.view.window['-folder-'].get()

                    app.add_coin(selected_exc, coin_name, abbr,
                                 start_date, start_hour, save_folder)

                    app.update_coin_tbl(selected_exc)

        # User clicks update button and data starts to download
        if event == '-update_coin-':
            if not selected_coin:
                app.display('*Select Coin')
            else:
                col_num = values['-coin_table-'][0]
                selected_coin = selected_exc.coins[col_num]
                app.download_data(selected_coin)

        # User clicks update all button and all data starts to download
        if event == '-update_all-':
            for coin in selected_exc.coins:
                app.download_data(coin)
                app.update_coin_tbl(selected_exc)

        # User clicks delete button and coin data is deleted
        if event == '-delete_coin-':
            if not selected_coin:
                app.display('*Select Coin')
            else:
                col_num = values['-coins_table-'][0]
                selected_coin = selected_exc.coins[col_num]
                app.delete_coin(selected_coin)
                app.update_coin_tbl(selected_exc)

    app.view.window.close()


if __name__ == "__main__":
    run()
