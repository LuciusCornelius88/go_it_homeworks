from interface import InterfaceClient


def main():
    interface = InterfaceClient()
    interface.represent_commands_list()
    interface.handle_command()


if __name__ == '__main__':
    main()
