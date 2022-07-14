from contacts_assistant.code.main_contacts_assist import main as main_book
from files_sorter.main_sorter import main as main_sorter
from notes_manager.notes import main as main_notes


def main():
    answ = ''
    while True:
        answ = input('Enter "Phone" to work with AddressBook.\n'
                     'Enter "Notes" to work with NotesManager.\n'
                     'Enter "Clear" to run the FolderSorter.\n'
                     'Enter "Exit" to shut down the app:\n')
        if answ == 'Phone':
            main_book()
        elif answ == 'Notes':
            main_notes()
        elif answ == 'Clear':
            main_sorter()
        elif answ == 'Exit':
            print('Good bye!')
            break
        else:
            print('Please, make your choice. And try again.')
            continue


if __name__ == '__main__':
    main()
