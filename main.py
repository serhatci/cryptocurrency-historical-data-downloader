import PySimpleGUI as sg  # GUI framework library
from screen_layout import Layout
from model_view_controller import Controller, Model, View
from exchange_base_cls import Exchange
from exchange_classes import *


def run(app):
    """Executes the application.

    Args:
        app (object): controller object of MVC
    """

    # Initializes all exchange classes in exchange_classes.py
    app.exc_list = [cls() for cls in Exchange.__subclasses__()]

    # Creates the start screen layout
    layout = Layout.create(app.exc_list)

    # Initializes start screen attaches it to app.view
    app.view.window = sg.Window('Crypto-exchanges Data Downloader',
                                layout,
                                size=(1000, 500),
                                finalize=True)

    # Listens the screen and collect user inputs
    while True:
        event, values = app.view.window.read()

        # Terminate app when user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        # Displays info when a listed exchange was clicked
        if event == '-exchanges_table-':
            col_num = values['-exchanges_table-'][0]
            app.selected_exc = app.exc_list[col_num]
            msg = f'{app.selected_exc.name}\n-----\n' \
                f'{app.selected_exc.website}'
            app.display(msg, 'green')

        # User clicks -add- button and a new coin is added
        if event == '-add_coin-':
            if not values['-exchanges_table-']:
                app.display('*Select Exchange')
            else:
                if not values['-coin_name-'] and values['-abbr-']:
                    app.display('*Missing Info')
                else:
                    coin_name = values['-coin_name-']
                    abbr = values['-abbr-']
                    start_date = values['-start_date-']
                    start_hour = values['-start_hour-']
                    app.add_coin(coin_name, abbr, start_date, start_hour)

        # User clicks update button and data starts to download
        if event == '-update_coin-':
            if not values['-coins_table-']:
                app.display('*Select Coin')
            else:
                col_num = values['-coins_table-'][0]
                app.selected_coin = app.selected_exc.coin_list[col_num]
                app.download_data(app.selected_coin)

        # User clicks update all button and all data starts to download
        if event == '-update_all-':
            for coin in app.selected_exc.coin_list:
                app.download_data(coin)

        # User clicks delete button and coin data is deleted
        if event == '-delete_coin-':
            if not values['-coins_table-']:
                app.display('*Select Coin')
            else:
                col_num = values['-coins_table-'][0]
                app.selected_coin = app.selected_exc.coin_list[col_num]
                app.delete_coin(app.selected_coin)

    app.view.window.close()


if __name__ == "__main__":
    app = Controller(Model(), View())
    run(app)
