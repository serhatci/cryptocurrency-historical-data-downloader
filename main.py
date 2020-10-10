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

    # Initializes start screen window object
    window = sg.Window('Crypto-exchanges Data Downloader',
                       layout,
                       size=(1000, 500),
                       finalize=True)

    # Listens the screen and collect user inputs
    while True:
        event, values = window.read()

        # Terminate app when user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        # Displays info when a listed exchange was clicked
        if event == '-exchanges_table-':
            col_num = values['-exchanges_table-'][0]
            app.selected_exchange = app.exc_list[col_num]
            app.show_exc_info(app.selected_exchange)
            app.refresh_coin_table(window, app.selected_exchange)

        # User clicks -add- button and a new coin is added
        if event == '-add_coin-':
            if not values['-exchanges_table-']:
                app.warning_select_exc(window)
            else:
                if not values['-coin_name-'] and values['-abbr-']:
                    app.warning_fill_inputs(window)
                else:
                    app.add_coin_to(app.selected_exchange)
                    app.refresh_coin_table(window, app.selected_exchange)
                    app.warning_coin_added(window)

        # User clicks update button and data starts to download
        if event == '-update_coin-':
            if not values['-coins_table-']:
                app.warning_select_coin(window)
            else:
                col_num = values['-coins_table-'][0]
                app.selected_coin = app.selected_exchange.coin_list[col_num]
                app.upload_coin(app.selected_coin)
                app.refresh_coin_table(window, app.selected_exchange)
                app.warning_update_coin(window)

        # User clicks update all button and all data starts to download
        if event == '-update_all-':
            for coin in app.selected_exchange.coin_list:
                app.upload_coin(coin)

            app.refresh_coin_table(window, app.selected_exchange)
            app.warning_update_all(window)

        # User clicks delete button and coin data is deleted
        if event == '-delete_coin-':
            if not values['-coins_table-']:
                app.warning_select_coin(window)
            else:
                col_num = values['-coins_table-'][0]
                app.selected_coin = app.selected_exchange.coin_list[col_num]
                app.delete_coin(app.selected_coin)
                app.refresh_coin_table(window, app.selected_exchange)
                app.warning_update_all(window)

    window.close()


if __name__ == "__main__":
    app = Controller(Model(), View())
    run(app)