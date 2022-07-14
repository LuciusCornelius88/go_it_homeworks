from pathlib import Path
from contacts_assistant.code.client_interface_classes import FirstOrderInterfaceClient


def main():
    filepath = Path(__file__).parents[1] / 'objects_copy.bin'
    interface = FirstOrderInterfaceClient(filepath)
    interface.represent_commands_list()
    interface.handle_command()


# if __name__ == '__main__':
#     main()
