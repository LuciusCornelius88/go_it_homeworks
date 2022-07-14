from enum import Enum
from contacts_assistant.code.parsers import CommandsParser


class FirstOrderCommands(Enum):

    HELLO = 'hello'
    BYE = 'good_bye'
    CLOSE = 'close'
    EXIT = 'exit'
    ADD = 'add_record'
    GET = 'get_record'
    CHANGE = 'change_record'
    DELETE = 'delete_record'
    SEARCH = 'search_records'
    SHOW = 'show_records'
    ALL = 'show_all'
    BIRTHDAYS = 'birthday_soon'
    SAVE = 'save'
    REPR_COMMDS = 'represent_commands'


class SecondOrderCommands(Enum):

    EXIT = 'exit'
    ADD_PHONE = 'add_phone'
    ADD_EMAIL = 'add_email'
    ADD_ADDRESS = 'add_address'
    ADD_BD = 'add_birthday'
    CH_PHONE = 'change_phone'
    CH_EMAIL = 'change_email'
    CH_ADDRESS = 'change_address'
    CH_BD = 'change_birthday'
    DEL_PHONE = 'delete_phone'
    DEL_EMAIL = 'delete_email'
    DEL_BD = 'delete_birthday'
    DEL_ADDRESS = 'delete_address'
    CH_REC_NAME = 'change_record_name'
    REPR_COMMDS = 'represent_commands'


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
