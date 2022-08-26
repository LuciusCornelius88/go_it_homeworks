from pathlib import Path
from decorators import errors_handler
from commands_handler import CommandsHandler, Commands
from queries import change_name, add_phone, change_phone, delete_phone, add_email, \
    change_email, delete_email, add_address, change_address, delete_address, \
    change_birthday, delete_birthday, get_record, add_record, delete_record, \
    birthday_soon, show_all, show_n_records, delete_none


# -------------PROMPT_TOOLKIT-------------
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


class Interface:

    def hello(self):
        return 'Hello!'

    def exit(self):
        print('Good bye!')
        return 'exit'

    def represent_commands(self):
        representer = RepresentCommands()
        return representer.represent()

    # KeyError_(No_Such_Command)
    def commands_handler(self, command: str):
        COMMANDS = {
            'hello': self.hello,
            'good_bye': self.exit,
            'close': self.exit,
            'exit': self.exit,
            'add_record': add_record,
            'get_record': get_record,
            'delete_record': delete_record,
            'delete_none': delete_none,
            'show_n_records': show_n_records,
            'show_all': show_all,
            'birthday_soon': birthday_soon,
            'change_name': change_name,
            'add_phone': add_phone,
            'add_email': add_email,
            'add_address': add_address,
            'add_birthday': change_birthday,
            'change_phone': change_phone,
            'change_email': change_email,
            'change_address': change_address,
            'change_birthday': change_birthday,
            'delete_phone': delete_phone,
            'delete_email': delete_email,
            'delete_birthday': delete_birthday,
            'delete_address': delete_address,
            'represent_commands': self.represent_commands
        }

        return COMMANDS[command]


# ParseException
class InterfaceClient:

    def __init__(self):
        self.interface = Interface()
        self.message_representer = RepresentCommands()
        self.completer = WordCompleter(self.message_representer.commands)

    def represent_commands_list(self):
        print(self.message_representer.represent())

    @errors_handler
    def handle_command(self):
        while True:
            command = CommandsHandler(prompt(
                'Please, enter command: ',
                history=FileHistory(
                    Path(__file__).parents[1] / 'history.txt'),
                auto_suggest=AutoSuggestFromHistory(),
                completer=self.completer,
                style=style
            )).parse_commands()

            function = self.interface.commands_handler(command)
            result = function()
            if result == 'exit':
                break
            elif isinstance(result, list):
                for res in result:
                    print(res)
                    print()
            else:
                print(result)


class RepresentCommands():

    def __init__(self):
        self.commands = [i.value for i in Commands]
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

        return '\nYou can use next commands:'+'\n' + self.string
