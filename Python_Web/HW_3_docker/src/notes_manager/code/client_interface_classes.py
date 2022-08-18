from pathlib import Path
from notes_manager.code.decorators import errors_handler
from notes_manager.code.commands_representers import RepresentFirstOrderCommands, \
    RepresentSecondOrderCommands
from notes_manager.code.notes_classes import Note
from notes_manager.code.notebook_classes import NoteBook
from notes_manager.code.commands_handler import CommandsHandler


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

    def __init__(self, note: Note, note_book: NoteBook):
        self.note_book = note_book
        self.note = note

    def exit(self):
        print('Note handling is done. Return to handling with note book.')
        return 'exit'

    def represent_commands(self):
        representer = RepresentSecondOrderCommands()
        return representer.represent()

    @errors_handler
    def change_note_id(self):
        note = self.note_book.get_note()
        if not isinstance(note, Note):
            return note
        self.note = note
        return f'Note to handle with was changes to {self.note.topic.value}, id: {self.note.id}'

    # KeyError_(No_Such_Command)
    def commands_handler(self, command: str):
        COMMANDS = {
            'exit': self.exit,
            'add_tag': self.note.add_tag,
            'change_topic': self.note.change_topic,
            'change_text': self.note.change_text,
            'change_tag': self.note.change_tag,
            'delete_tag': self.note.delete_tag,
            'delete_text': self.note.delete_text,
            'get_updates': self.note.get_updates,
            'change_note_id': self.change_note_id,
            'represent_commands': self.represent_commands,
            'save': self.note_book.save_to_file
        }

        return COMMANDS[command]


# ParseException
class SecondOrderInterfaceClient:

    def __init__(self, note: Note, note_book: NoteBook):
        self.interface = SecondOrderInterface(note, note_book)
        self.message_representer = RepresentSecondOrderCommands()
        self.completer = WordCompleter(self.message_representer.commands)

    def represent_commands_list(self):
        print(self.message_representer.represent())

    @errors_handler
    def handle_command(self):
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
            self.note_book = NoteBook(self.filepath).restore_from_file()
            print('Note book was restored from objects_copy.bin')
        except (EOFError, FileNotFoundError):
            self.note_book = NoteBook(filepath)
            print('New note book was created.')

    def hello(self):
        return 'Hello!'

    def exit(self):
        self.note_book.save_to_file()
        print('Note book was saved to objects_copy.bin. Good bye!')
        return 'exit_first_order'

    def represent_commands(self):
        representer = RepresentFirstOrderCommands()
        return representer.represent()

    @errors_handler
    def second_order_interface(self):
        note = self.note_book.get_note()
        if not isinstance(note, Note):
            return note
        interface = SecondOrderInterfaceClient(note, self.note_book)
        interface.represent_commands_list()
        result = interface.handle_command()
        return result

    # KeyError_(No_Such_Command)
    def commands_handler(self, command: str):
        COMMANDS = {
            'hello': self.hello,
            'good_bye': self.exit,
            'close': self.exit,
            'exit': self.exit,
            'add_note': self.note_book.add_note,
            'get_note': self.note_book.get_note,
            'delete_note': self.note_book.delete_note,
            'sort_by_topic': self.note_book.sort_notes_by_topic,
            'sort_by_tag': self.note_book.sort_notes_by_tag,
            'show_notes': self.note_book.iterate,
            'show_all': self.note_book.show_all,
            'save': self.note_book.save_to_file,
            'change_note': self.second_order_interface,
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
