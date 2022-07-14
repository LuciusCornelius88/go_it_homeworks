import initial_data
from my_decorators import input_error_decorator


# БЛОК МЕТОДОВ ДЛЯ ОБРАБОТКИ КОМАНД


def handle_hello():
    print('How can I help you?')


@input_error_decorator
def handle_add(*args):
    name, phone = args
    if initial_data.contacts_list.get(name, None):
        raise ValueError()
    initial_data.contacts_list[name] = phone
    print('Done!')


@input_error_decorator
def handle_change(*args):
    name, phone = args
    if not initial_data.contacts_list.get(name, None):
        raise ValueError()
    initial_data.contacts_list[name] = phone
    print('Done!')


@input_error_decorator
def handle_phone(name):
    if not initial_data.contacts_list.get(name, None):
        raise ValueError()
    print(initial_data.contacts_list[name])


def handle_show_all():
    if not initial_data.contacts_list:
        print('There are no contacts in your phonebook!')
    else:
        for key, val in initial_data.contacts_list.items():
            print(f'name: {key}; phone: {val}')


def handle_exit():
    print('Good_by!')
    return '.'


COMMANDS = {
    'hello': handle_hello,
    'add': handle_add,
    'change': handle_change,
    'phone': handle_phone,
    'show all': handle_show_all,
    'good bye': handle_exit,
    'close': handle_exit,
    'exit': handle_exit
}


@input_error_decorator
def commands_handler(command):
    return COMMANDS[command]
