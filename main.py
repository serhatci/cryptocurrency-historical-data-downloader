from config_cls import Config
from model_view_controller import Controller, Model, View

if __name__ == "__main__":
    """Executes the application.
    """
    # Instantiate application object
    app = Controller(Model(Config()), View())
    app.start()
