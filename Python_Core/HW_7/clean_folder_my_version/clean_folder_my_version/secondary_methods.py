import os
import re
import shutil
from pathlib import Path

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
    # 2) в методе move_files(path, count) при перемещении файлов в корневую директорию, на 1й уровень


def handle_duplicates(name, lst):
    if name in lst:
        name, extens = name.split('.')
        new_name = f'{name}_copie.{extens}'
        return handle_duplicates(new_name, lst)
    else:
        return name
