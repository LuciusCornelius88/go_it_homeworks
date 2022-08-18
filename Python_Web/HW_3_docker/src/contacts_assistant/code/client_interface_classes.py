from pathlib import Path
from contacts_assistant.code.decorators import errors_handler
from contacts_assistant.code.commands_representers import RepresentFirstOrderCommands, \
    RepresentSecondOrderCommands
from contacts_assistant.code.record_classes import Record
from contacts_assistant.code.address_book_classes import AddressBook
from contacts_assistant.code.commands_handler import CommandsHandler

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


class SecondOrderInterface:

    def __init__(self, record: Record, address_book: AddressBook):
        self.address_book = address_book
        self.record = record

    def exit(self):
        print('Record handling is done. Return to handling with Address book.')
        return 'exit'

    def represent_commands(self):
        representer = RepresentSecondOrderCommands()
        return representer.represent()

    @errors_handler
    def change_record_name(self):
        record = self.address_book.get_record()
        if not isinstance(record, Record):
            return record
        self.record = record
        return f'Record to handle with was changes to {self.record.name.value.upper()}'

    # KeyError_(No_Such_Command)
    def commands_handler(self, command: str):
        COMMANDS = {
            'exit': self.exit,
            'add_phone': self.record.add_phone,
            'add_email': self.record.add_email,
            'add_address': self.record.change_address,
            'add_birthday': self.record.change_birthday,
            'change_phone': self.record.change_phone,
            'change_email': self.record.change_email,
            'change_address': self.record.change_address,
            'change_birthday': self.record.change_birthday,
            'delete_phone': self.record.delete_phone,
            'delete_email': self.record.delete_email,
            'delete_birthday': self.record.delete_birthday,
            'delete_address': self.record.delete_address,
            'change_record_name': self.change_record_name,
            'represent_commands': self.represent_commands
        }

        return COMMANDS[command]


# ParseException
class SecondOrderInterfaceClient:

    def __init__(self, record: Record, address_book: AddressBook):
        self.interface = SecondOrderInterface(record, address_book)
        self.message_representer = RepresentSecondOrderCommands()
        self.completer = WordCompleter(self.message_representer.commands)

    def represent_commands_list(self):
        print(self.message_representer.represent())

    @errors_handler
    def handle_command(self):
        print(self.message_representer.represent())

        while True:
            command = CommandsHandler(prompt(
                'Please, enter second_order_command: ',
                history=FileHistory(
                    Path(__file__).parents[1] / 'history.txt'),
                auto_suggest=AutoSuggestFromHistory(),
                completer=self.completer,
                style=style
            )).parse_second_order_commands()

            function = self.interface.commands_handler(command)
            result = function()
            if result == 'exit':
                break
            else:
                print(result)
        return 'exit_second_order'


class FirstOrderInterface:

    def __init__(self, filepath):
        self.filepath = filepath
        try:
            self.address_book = AddressBook(self.filepath).restore_from_file()
            print('Address book was restored from objects_copy.bin')
        except (EOFError, FileNotFoundError):
            self.address_book = AddressBook(filepath)
            print('New Address book was created.')

    def hello(self):
        return 'Hello!'

    def exit(self):
        self.address_book.save_to_file()
        print('Address book was saved to objects_copy.bin. Good bye!')
        return 'exit_first_order'

    def represent_commands(self):
        representer = RepresentFirstOrderCommands()
        return representer.represent()

    @errors_handler
    def second_order_interface(self):
        record = self.address_book.get_record()
        if not isinstance(record, Record):
            return record
        interface = SecondOrderInterfaceClient(record, self.address_book)
        result = interface.handle_command()
        return result

    # KeyError_(No_Such_Command)
    def commands_handler(self, command: str):
        COMMANDS = {
            'hello': self.hello,
            'good_bye': self.exit,
            'close': self.exit,
            'exit': self.exit,
            'add_record': self.address_book.add_record,
            'get_record': self.address_book.get_record,
            'delete_record': self.address_book.delete_record,
            'search_records': self.address_book.search_records,
            'birthday_soon': self.address_book.find_soonest_bd,
            'show_records': self.address_book.iterate,
            'show_all': self.address_book.show_all,
            'save': self.address_book.save_to_file,
            'change_record': self.second_order_interface,
            'represent_commands': self.represent_commands
        }

        return COMMANDS[command]


# ParseException
class FirstOrderInterfaceClient:

    def __init__(self, filepath):
        self.interface = FirstOrderInterface(filepath)
        self.message_representer = RepresentFirstOrderCommands()
        self.completer = WordCompleter(self.message_representer.commands)

    def represent_commands_list(self):
        print(self.message_representer.represent())

    @errors_handler
    def handle_command(self):
        while True:
            command = CommandsHandler(prompt(
                'Please, enter first_order_command: ',
                history=FileHistory(
                    Path(__file__).parents[1] / 'history.txt'),
                auto_suggest=AutoSuggestFromHistory(),
                completer=self.completer,
                style=style
            )).parse_first_order_commands()

            function = self.interface.commands_handler(command)
            result = function()
            if result == 'exit_first_order':
                break
            elif result == 'exit_second_order':
                continue
            else:
                print(result)
