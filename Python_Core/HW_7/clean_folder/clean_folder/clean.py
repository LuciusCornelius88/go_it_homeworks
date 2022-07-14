import re
import os
import shutil
from sys import argv
from pathlib import Path

# код с исходными структурами данных
extens_types = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'XMIND'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}

images = []
video = []
documents = []
audio = []
archives = []
unknown_files = []

known_extens = []
unknown_extens = []

# основной результат данной части кода - создание словаря типа {'images' : list_of_images[]}
filename_lists = [images, video, documents, audio, archives]
lists_of_files = dict(zip(extens_types.keys(), filename_lists))

# метод для рекурсивного прохождения по файловой системе переданной директории, формирования:
# 1) словаря типа {'images' : [namelist of images]}
# 2) списка с именами файлов с неизвестными расширениями
# 3) списка с уникальными известными расширениями
# 4) списка с уникальными неизвестными расширениями


def scan_dir(path):
    for elem in path.iterdir():
        # метка для отслеживания того, имеет ли файл неизвестное расширение;
        # по умолчанию семафор "включен", как в случае с неизвестным расширением
        flag = True

        # рекурсивно обходим папки, нормализуем их названия и переименовываем их
        if elem.is_dir():
            scan_dir(elem)
            name = normalize(elem.name)
            os.rename(elem, Path(path, name))

        # для файлов: нормализуем их имена, переименовываем, получаем расширение и приводим к заданному формату (upper())
        else:
            name = normalize(elem.name)
            extens = name.split('.')[1].upper()
            os.rename(elem, Path(path, name))

            # имена в полном формате (дял облегчения их последующей сортировки методом sort_files()) добавляем в словарь
            # lists_of_files
            for key, val in extens_types.items():
                if extens in val:
                    # "выключаем" семафор после нахождения файла с известным расширением
                    flag = False

                    # если имена повторяются, прогоняем их через специальный метод handle_duplicates() (подробности см. ниже)
                    if name in lists_of_files[key]:
                        name = handle_duplicates(name, lists_of_files[key])
                        lists_of_files[key].append(name)
                    else:
                        lists_of_files[key].append(name)

                    # расширение добавляем в отдельный список для последующего отчета скрипта о проделанной работе
                    if extens not in known_extens:
                        known_extens.append(extens)

            # та же логика для файлов с неизвестными расширениями: имена прогоняем, в случае надопности,
            # через handle_duplicates() (подробности см. ниже); расширение добавляем в отдельный список
            # для последующего отчета скрипта о проделанной работе
            if flag:
                if name in unknown_files:
                    name = handle_duplicates(name, unknown_files)
                    unknown_files.append(name)
                else:
                    unknown_files.append(name)

                if extens not in unknown_extens:
                    unknown_extens.append(extens)

# метод для нормализации (перевода) кириллических названий файлов и папок в латинские
# с заменой всех небуквенных символов на '_'


def normalize(name):
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ja", "je", "i" "ji", "g")

    trans = {}

    for kyr, lat in zip(cyrillic_symbols, translation):
        trans[ord(kyr)] = lat
        trans[ord(kyr.upper())] = lat.upper()

    # в метод передаем полное имя типа 'name.extens', поэтому сперва разбиваем его на 2 части и нормализуем только name;
    # возвращаем тоже имя типа 'name.extens', созданное конкатенацией нормализованного имени с сохраненным
    # в исходном виде расширением
    name, extens = os.path.splitext(name)

    norm_name = re.sub('\W', '_', name.translate(trans)) + extens

    return norm_name

# в этом методе наша задача состоит в том, чтобы рекурсивно пройти по всем папкам и "поднять" все файлы
# в корневую папку (на 1й уровень); отдельные задачи:
    # 1) использовать метод handle_duplicates(name, current_list) для того, чтобы файлы с повторяющимися именами не удалялись,
    # а изменялись из вида 'name.extens' в вид 'name_copie.extens'
    # 2) использовать счетчик count, чтобы файлы, уже находящиеся на 1м уровне (count=0), не сравнивались сами с собой
    # и не прогонялись через handle_duplicates() (при тестирвоании использовались файлы 'Viber.lnk' и 'Slack.lnk');
    # через handle_duplicates() прогоняем только файлы во вложенных папках


def move_files(path, count=0):
    for elem in path.iterdir():
        if elem.is_dir():
            # при уходе в глубину системы папок, увеличиваем count, и тогда на вложенных уровнях имена файлов сравниваются
            # с уже имеющимися файлами 1го уровня
            count += 1
            move_files(elem, count)
            # при "раскручивании" рекурсии, постепенно уменьшаем count до 0, чтобы при возвращении на 1й уровень
            # находящиеся там файлы не сравнивались со списком файлов 1го уровня, где они изначально были
            count -= 1
            os.rmdir(elem)
        else:
            current_list = os.listdir(Path.cwd())

            if elem.name in current_list and count > 0:
                name = handle_duplicates(elem.name, current_list)
                os.replace(elem, Path(Path.cwd(), name))
            else:
                os.replace(elem, Path(Path.cwd(), elem.name))

# после того, как мы "подняли" все файлы из папок в корневую папку (на 1й уровень), наша задача состоит в том, чтобы:
    # 1) создать целевые папки для сортировки файлов (images, video etc.)
    # 2) рассортировать файлы по этим папкам на основании полученного в методе scan_dir(path)
        # lists_of_files словаря, в котором хранятся данные типа {'images' : list_of_images['name.extens', 'name_extens'...]}
    # 3) обработать отдельным методом архивы
    # 4 отсортировать в отдельную папку файлы с неизвестным расширением


def sort_files(path, lists_of_files, unknown_files):
    for key, val in lists_of_files.items():
        os.mkdir(Path(path, key))

        for item in val:
            if key == 'archives':
                handle_archives(path, key, item)
            else:
                os.replace(Path(path, item), Path(path, key, item))

    handle_unknown(path, unknown_files)

# обработку файлов неизвестного формата (создание папки 'unknown_files' и перемещение туда всех файлов
# с неизвестным расширением) для удобства выносим в отдельный метод;
# данный метод вызывается в методе sort_files(path, lists_of_files, unknown_files)


def handle_unknown(path, unknown_files):
    dir_name = 'unknown_files'
    os.mkdir(Path(path, dir_name))

    for item in unknown_files:
        os.replace(Path(path, item), Path(path, dir_name, item))

# обработку архивов (распаковку в папку 'archive\\archive_name' и удаление архива) для удобства выносим в отдельный метод;
# данный метод вызывается в методе sort_files(path, lists_of_files, unknown_files)


def handle_archives(path, key, item):
    archive_name = item.split('.')[0]
    shutil.unpack_archive(Path(path, item), Path(path, key, archive_name))
    os.remove(Path(path, item))

# метод для обработки повторяющихся имен; идея в том, что в неотсортированных каталогах могут находиться файлы
# с одинаковыми именами; я хочу, чтобы все эти файлы были "подняты" на верхний уровень и отсортированы в соответствующую папку;
# по умолчанию, все файлы с одинаковым именем удаляются, остается только один экземпляр;
# чтобы этого избежать, добавляется функция, которая
    # 1) меняет имя файла формата 'name.extens' в формат 'name_copie.extens';
    # 2) рекурсивно вызывает себя, сравнивая новое имя с существующими в целевой папке.
# Данный метод используется в 2х местах программы:
    # 1) в методе scan_dir(path) при формировании словаря имен файлов;
    # 2) в методе move_files(path, count) при перемещении файлов в корневую директорию, на 1й уровенm


def handle_duplicates(name, lst):
    if name in lst:
        name, extens = name.split('.')
        new_name = f'{name}_copie.{extens}'
        return handle_duplicates(new_name, lst)
    else:
        return name

# метод для красивого вывода результатов работы скрипта


def print_results():
    print('Filenames with unknown extension:')
    for i in unknown_files:
        if unknown_files.index(i) < (len(unknown_files)-1):
            print('{:10}{:<30}'.format('', i))
        else:
            print('{:10}{:<30}\n'.format('', i))

    print(f'Unique known extensions: {known_extens}')
    print(f'Unique unknown extensions: {unknown_extens}\n')

    for key, val in lists_of_files.items():
        print('{:<10}'.format(key+':'))
        for item in val:
            print('{:10}{:<50}'.format('', item))

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
    scan_dir(path)
    move_files(path)
    sort_files(path, lists_of_files, unknown_files)

    # вывод отчета о проделанной работе скрипта
    print_results()

    # меняем адрес домашней директории на родительский относительно переденного пути, чтобы папку можно было изменить/удалить
    new_path = os.path.dirname(path)
    os.chdir(new_path)


# задаем точку входа
if __name__ == '__main__':
    main()
