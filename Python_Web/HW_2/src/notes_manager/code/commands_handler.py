from enum import Enum
from notes_manager.code.parsers import CommandsParser


class FirstOrderCommands(Enum):

    HELLO = 'hello'
    BYE = 'good_bye'
    CLOSE = 'close'
    EXIT = 'exit'
    ADD = 'add_note'
    GET = 'get_note'
    CH = 'change_note'
    DEL = 'delete_note'
    SORT_TOP = 'sort_by_topic'
    SORT_TAG = 'sort_by_tag'
    SHOW = 'show_notes'
    ALL = 'show_all'
    SAVE = 'save'
    REPR_COMMDS = 'represent_commands'


class SecondOrderCommands(Enum):

    EXIT = 'exit'
    ADD_TAG = 'add_tag'
    CH_TOP = 'change_topic'
    CH_TXT = 'change_text'
    CH_TAG = 'change_tag'
    DEL_TAG = 'delete_tag'
    DEL_TXT = 'delete_text'
    GET_UPT = 'get_updates'
    CH_NOTE_ID = 'change_note_id'
    REPR_COMMDS = 'represent_commands'
    SAVE = 'save'


class CommandsSorter:

    def __init__(self):
        self.dict_of_commands = dict()

    def sort_commands(self, string_items: list, commands: list) -> tuple:
        uscore_joined_string = '_'.join(string_items)
        solid_joined_string = ''.join(string_items)

        for command in commands:
            if command in uscore_joined_string and command not in self.dict_of_commands:
                index = uscore_joined_string.find(command)
                self.dict_of_commands[index] = command
            elif command.replace('_', '') in solid_joined_string and command not in self.dict_of_commands:
                index = solid_joined_string.find(command.replace('_', ''))
                self.dict_of_commands[index] = command
            else:
                continue

        sorted_matched_positions = sorted(self.dict_of_commands.keys())

        return sorted_matched_positions, self.dict_of_commands


class CommandsExtractor:

    def get_command(self, posits_of_commands: list, indexed_commands: dict):

        if len(posits_of_commands) > 1 and indexed_commands[posits_of_commands[0]] == 'hello':
            return indexed_commands[posits_of_commands[1]]
        elif not posits_of_commands:
            return None
        else:
            return indexed_commands[posits_of_commands[0]]


class CommandsHandler:

    def __init__(self, string: str):
        self.parser = CommandsParser(string)
        self.sorter = CommandsSorter()
        self.extractor = CommandsExtractor()

    def parse_string(self, commands: list) -> str:
        string_items = self.parser.parse_string()
        posits_of_commands, indexed_commands = self.sorter.sort_commands(
            string_items, commands)
        command = self.extractor.get_command(
            posits_of_commands, indexed_commands)
        return command

    def parse_first_order_commands(self) -> str:
        commands = [command.value for command in FirstOrderCommands]
        return self.parse_string(commands)

    def parse_second_order_commands(self) -> str:
        commands = [command.value for command in SecondOrderCommands]
        return self.parse_string(commands)
