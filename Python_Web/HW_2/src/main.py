from contacts_assistant.code.main_contacts_assist import main as main_book
from files_sorter.main_sorter import main as main_sorter
from notes_manager.code.main_notes_manager import main as main_notes


def handle_initial_command(command: str):
    COMMANDS = {
        'phone': main_book,
        'clear': main_sorter,
        'notes': main_notes
    }
    return COMMANDS[command]


def main():
    while True:
        command = input('Enter "phone" to work with contacts_assistant.\n\
            Enter "clear" to work with directory_sorter.\n\
            Enter "notes" to work with notes_manager.\n\
            Or enter "close" to exit the programm:\n')

        if command == 'close':
            print('Good bye!')
            break

        try:
            prog = handle_initial_command(command)
            prog()
        except KeyError:
            print('There is no such command. Please, try again!')


if __name__ == '__main__':
    main()
