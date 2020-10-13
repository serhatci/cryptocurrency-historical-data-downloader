class Controller():
    """Controller class of MVC design.
    """

    def __init__(self, model, view):
        """Constructor of Controller class.

        Args:
            model (object): model of MVC design
            view (object): view of MVC design
        """
        self.model = model
        self.view = view

    def refresh_coin_table(self, selected_exc):
        pass

    def add_coin(self, selected_exc, coin_name, abbr,
                 start_date, start_hour, file_directory):

        self.model.add_coin()

        pass

    def delete_coin():
        pass

    def download_data():
        pass

    def display(self, text, color=None):
        """Sends messages to be displayed in action panel.

        Args:
            text (str): desired message to be displayed or selection 
                        of one of predefined messages below:
                            *Select Coin
                            *Select Exchange
                            *Missing Info
            color (str, optional): desired text colour(Defaults to None)

        Returns:
            method: calls display method of View class 
        """
        if not color:
            text, color = PredefinedMessages.get(text)
        return self.view.display(text, color)


class Model:
    """ Model class of MVC design.
    """
    pass


class View:
    """ View class of MVC design.

    attr:
        window (obj): Pysimplegui window object
    """

    window = None

    def display(self, msg, color):
        """Displays messages on action panel in the screen.

        Args:
            msg (str): desired message to be displayed
            color (str): desired color of the message
        """
        self.window['-action_panel_multiline-'].update(msg, text_color=color)
    pass


class PredefinedMessages:
    """Contains pre-defined messages to select among them.

    Class Attr:
        messages [dict]: dictionary of pre-defined messages
                         which users can select among them 
    """

    messages = {'*Select Exchange':
                ['Please select an exchange first!..',
                 'red'],
                '*Select Coin':
                ['Please select a coin first!..',
                 'red'],
                '*Missing Info':
                ['Please fill all necessary information!..',
                 'red']
                }

    @ classmethod
    def get(cls, text):
        """Provides pre-defined messages.

        Args:
            text (str): message title to be searched in messages
                        dictionary 

        Returns:
            text [str]: pre-defined message to be displayed
            color [str]: color of the message
        """
        for key, value in cls.messages.items():
            if key == text:
                text, color = value
                return text, color
                break
