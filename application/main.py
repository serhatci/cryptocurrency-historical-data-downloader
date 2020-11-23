"""Executes the application.

Contact:
--------
- start.a.foolish.huge.project@gmail.com

More information is available at:
- https://github.com/serhatci/cryptocurrency-historical-data-downloader
- https://pypi.org/project/cryptoasset-data-downloader/

Version:
--------
- cryptoasset-data-downloader v1.0.8
"""
from application.model_view_controller import Controller, Model, View


def run():
    # Instantiate application object
    app = Controller(Model(), View())

    # Starts execution of app
    app.start_app()


if __name__ == "__main__":
    run()
