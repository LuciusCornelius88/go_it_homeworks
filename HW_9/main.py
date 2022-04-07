import parser
import handlers


def main():
    print('''Hello! I\'m your virtual assistant. Some words about how I can assist you:
        1) print "add name phone_number" to add a new contact to your contacts list;
        2) print "change name phone_number" to change the existing contact;
        3) print "phone name" to search for a phone_number of existing contact;
        4) print "show all" to display all the contacts, saved in the contacts list;
        5) print "good bye" or "close" or "exit" to finish working with me and close the session.''')

    while True:
        exit_point = '.'
        string = input()

        if string == exit_point:
            print('Good bye!')
            break

        args = parser.string_parser(string)

        if isinstance(args, list):
            command = args[0]
            args = args[1:]
            handler = handlers.commands_handler(command)
            handler(*args)
        elif args == None:
            continue
        else:
            handler = handlers.commands_handler(args)
            if handler() == exit_point:
                break


if __name__ == '__main__':
    main()
