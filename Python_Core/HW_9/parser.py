import re
import initial_data
from my_decorators import input_error_decorator

# ГРУППА МЕТОДОВ ДЛЯ ОБРАБОТКИ АРГУМЕНТОВ ВВОДА


# приводим номера телефонов к формату без пробелов, тире, знака "+" и скобок


def handle_phone_numbers(string):
    string = re.sub('[-+() ]', '', string)
    return string

# поиск имени = '\s\w+\s' (пробел; произвольное число букв, цифр и нижних подчеркиваний; пробел)
# поиск телефона = '[+]?(?:\d+[-() \d]+)\\b' (знак "+" или без него; произвольное число цифр;
# произвольное число чисел, или тире, или скобок, или пробелов; конец строки)


@input_error_decorator
def find_one_arg(command, string):
    args = re.search(f'{command}\s\w+\\b', string, re.IGNORECASE).group()
    args_list = args.split(' ')

    return args_list


@input_error_decorator
def find_two_args(command, string):
    args = re.search(
        f'{command}\s\w+\s[+]?(?:\d[-() \d]+)\\b', string, re.IGNORECASE).group()

    # "чистим" номер телефона
    phone_number = handle_phone_numbers(
        *re.findall('[+]?\\b(?:\d[-() \d]+)\\b', args))
    args = re.sub('[+]?\\b(?:\d[-() \d]+)\\b', phone_number, args)

    args_list = args.split(' ')

    return args_list


ARGS_NUMBER = {
    'phone': find_one_arg,
    'add': find_two_args,
    'change': find_two_args
}

# ГРУППА МЕТОДОВ ДЛЯ ПОИСКА КЛЮЧЕВОГО СЛОВА И АРГУМЕНТОВ ВВОДА

# здесь реализован дополнительный функционал; предположим, пользователь в одном вводе указывает несколько ключевых слов;
# тогда нужно установить между ними приоритеты; hello имеет более низкий приоритет; и если пользователь вместе с hello дает
# содержательную команду, то мы не выводим в ответ "Чем могу помочь?", а сразу выполняем основную команду;
# команды, имеющие высокий приоритет, приоритезируются в порядке поступления; так, выполнятся будет только первая из
# переданных основных команд; что касается команд, завершающих работу бота - они имеют высокий приоритет.


@input_error_decorator
def command_search(words_list):
    command = str()

    for item in words_list:
        if item in initial_data.first_order_commands:
            return item
        else:
            continue

    if not command:
        return words_list[0]

# поиск аргументов для полученной команды


@input_error_decorator
def args_search(command, string):
    args = ARGS_NUMBER[command]

    return args(command, string)

# ОСНОВНОЙ МЕТОД ПАРСЕРА


def string_parser(string):
    # объединяем ключевые слова из списка key_words через '|' (регулярный оператор ИЛИ), чтобы упростить регулярное выражение
    s = '|'.join(initial_data.key_words)

    # начало слова, одно из ключевых слов, конец слова
    key_words_found = re.findall(f'\\b(?:{s})\\b', string, flags=re.IGNORECASE)
    key_words_found = [item.lower() for item in key_words_found]

    command = command_search(key_words_found)

    if command in initial_data.commands_with_args:
        args = args_search(command, string)
        return args
    else:
        return command
