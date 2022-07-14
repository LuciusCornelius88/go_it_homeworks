import os
from pathlib import Path
from sys import argv
from clean_folder_my_version.main_methods import scan_dir, move_files, sort_files, print_results

# этот метод нужен на случай некорректного ввода адреса папки в командной строке; метод дает вводить
# адрес вручную до тех пор, пока не будет получен существующий адрес, указывающий на папку


def correct_input_test():
    while True:
        path = input("Enter correct Windows path: ")
        try:
            if os.path.exists(path) and os.path.isdir(path):
                return path
            else:
                continue
        except SyntaxError:
            continue


# метод для вызова основных функций скрипта


def main():
    # проверка корректности ввода адреса папки
    try:
        if os.path.exists(argv[1]) and os.path.isdir(argv[1]):
            path = Path(argv[1])
        else:
            path = Path(correct_input_test())
    except SyntaxError:
        path = Path(correct_input_test())

    # вызов основных методов
    os.chdir(path)
    unknown_files, known_extens, unknown_extens, lists_of_files = scan_dir(
        path)
    move_files(path)
    sort_files(path, lists_of_files, unknown_files)

    # вывод отчета о проделанной работе скрипта
    print_results(unknown_files, known_extens, unknown_extens, lists_of_files)

    # меняем адрес домашней директории на родительский относительно переденного пути,
    # чтобы папку можно было изменить/удалить
    new_path = os.path.dirname(path)
    os.chdir(new_path)


# задаем точку входа
if __name__ == '__main__':
    main()
