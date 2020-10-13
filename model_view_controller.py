class Controller():

    def __init__(self, model, view):
        self.model = model
        self.view = view
    pass

    def add_coin():
        pass

    def delete_coin():
        pass

    def download_data():
        pass

    def display(self, text, color=None):
        if not color:
            text, color = PredefinedMessages.get(text)
        return self.view.display(text, color)


class Model:
    pass


class View:

    def display(self, msg, color):
        self.window['-action_panel_multiline-'].update(msg, text_color=color)
    pass


class PredefinedMessages:

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
        for key, value in cls.messages.items():
            if key == text:
                text, color = value
                return text, color
                break
