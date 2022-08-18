from contacts_assistant.code.abstract_methods import RepresentObjects
from contacts_assistant.code.commands_handler import FirstOrderCommands, SecondOrderCommands


class RepresentFirstOrderCommands(RepresentObjects):

    def __init__(self):
        self.commands = [i.value for i in FirstOrderCommands]
        self.string = ''
        self.count = 0

    def represent(self):
        for command in self.commands:
            if self.commands[-1] == command:
                self.string += f'{command}.'
            elif self.count == 0:
                self.string += (' ') * 5 + f'{command}, '
                self.count += 1
            elif self.count < 4:
                self.string += f'{command}, '
                self.count += 1
            else:
                self.string += f'{command}\n'
                self.count = 0

        return '\nOn this level you can use next commands:'+'\n' + self.string


class RepresentSecondOrderCommands(RepresentObjects):

    def __init__(self):
        self.commands = [i.value for i in SecondOrderCommands]
        self.string = ''
        self.count = 0

    def represent(self):
        for command in self.commands:
            if self.commands[-1] == command:
                self.string += f'{command}.'
            elif self.count == 0:
                self.string += (' ') * 5 + f'{command}, '
                self.count += 1
            elif self.count < 4:
                self.string += f'{command}, '
                self.count += 1
            else:
                self.string += f'{command}\n'
                self.count = 0

        return '\nOn this level you can use next commands:'+'\n' + self.string
