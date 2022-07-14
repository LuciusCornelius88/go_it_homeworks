import re
import os
import shutil
from sys import argv
from pathlib import Path

# ОБРАБОТКА ВВОДА

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


try:
    if os.path.exists(argv[1]) and os.path.isdir(argv[1]):
        path = Path(argv[1])
    else:
        path = Path(correct_input_test())
except SyntaxError:
    path = Path(correct_input_test())

# делаем переданный путь домашним для того, чтобы можно было быстро получить доступ к целевым папкам
# при перемещении в них файлов в методе move_files
os.chdir(path)

# ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ
# задаем данные: делаем кортежи, чтобы можно было создать словарь, где ключи - это кортежи с типами данных,
# а значения - списки, в которые сортируем имена файлов
image_types = ('JPEG', 'PNG', 'JPG', 'SVG')
video_types = ('AVI', 'MP4', 'MOV', 'MKV')
doc_types = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
music_types = ('MP3', 'OGG', 'WAV', 'AMR')
archive_types = ('ZIP', 'GZ', 'TAR')

data_types = [image_types, video_types, doc_types, music_types, archive_types]

images = []
video = []
documents = []
audio = []
archives = []
unknown_type_files = []

data_lists = [images, video, documents, audio, archives]

file_lists_dict = dict(zip(data_types, data_lists))

known_extension_types = []
unknown_extension_types = []

# список имен новых папок, в которые сортируем файлы
dirs_to_create = ['images', 'video', 'documents', 'audio', 'archives']

# создаем в цикле новые папки
for dir_to_create in dirs_to_create:
    try:
        os.mkdir(Path(path, dir_to_create))
    except FileExistsError:
        continue

# метод, который 1) рекурсивно проходит по папкам, 2) переименовывает (нормализует) названия папок и файлов,
# 3) сортирует названия файлов и их расширений по соответствующим спискам,
# 4) возвращает словарь соответствий "тип файла - список имен файлов",
# 5) спосок файлов неизвествного типа, списки известных и неизвестных расширений файлов


def scan_directory(path):
    for i in path.iterdir():
        # семафор для отслежтивания того, встретился ли неизвестный тип данных после прогона цикла
        flag = False

        if i.is_dir():
            scan_directory(i)
            # нормализуем названия изначальных папок, исключая папки для сортировки файлов
            if i.name not in dirs_to_create:
                shutil.move(i, Path(path, normalize(i.name)))

        elif i.is_file():
            name = normalize(i.name)
            extension = os.path.splitext(i.name)[1].replace('.', '')
            # нормализуем названия файлов
            shutil.move(i, Path(path, name))

            # далее везде вставляем проверку на повторы имен файлов и расширений,
            # чтобы при повторных прогонах не добавлять уже добавленные значения; имя прогоняем через нормализующий метод
            for data_type in data_types:
                if extension.upper() in data_type:
                    if name not in file_lists_dict.get(data_type):
                        file_lists_dict.get(data_type).append(name)
                    if extension not in known_extension_types:
                        known_extension_types.append(extension)
                    # посел того, как нашли известный тип данный, "засвечиваем" семафор
                    flag = True

            # если семафор не засвечен, добавляем имена и расширения файлов в списки неизвестных расширений
            if not flag:
                if name not in unknown_type_files:
                    unknown_type_files.append(name)
                if extension not in unknown_extension_types:
                    unknown_extension_types.append(extension)

    sorted_file_names = dict(zip(dirs_to_create, file_lists_dict.values()))

    return (sorted_file_names,
            unknown_type_files,
            known_extension_types,
            unknown_extension_types)

# метод нормализации названий файлов и папок


def normalize(name):
    # словарь транслитерации
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ja", "je", "i" "ji", "g")

    trans = {}
    for cyr, lat in zip(cyrillic_symbols, translation):
        trans[ord(cyr)] = lat
        trans[ord(cyr.upper())] = lat.title()

    name_norm = os.path.splitext(name)[0]
    extension_norm = os.path.splitext(name)[1]

    # возвращаем имя, в котором кириллица транслитерирвоана на латиницу, а все нечислевые и небуквенные символы меняем на '_';
    # нормализуем только имя, расширение не трогаем, а в конце конкатенируем с нормализованным именем
    return re.sub('\W', '_', name_norm.translate(trans)) + extension_norm

# метод, который на основании полученного словаря с отсортированными именами файлов перемещает их в целевые папки,
# пустые папки удаляет, распаковывает архивы


def move_files(path, dict_of_files):
    for i in path.iterdir():
        # рекурсивно проходимся по папкам, кроме папок для сортировки
        if i.is_dir() and i.name not in dirs_to_create:
            move_files(i, dict_of_files)
            # блок кода для удаления пустых папок, если это не папки, созданные для сортировки файлов
            if len(os.listdir(i)) == 0 and i.name not in dirs_to_create:
                os.rmdir(i)

        elif i.is_file():
            for key, val in dict_of_files.items():
                if i.name in val:
                    # если рассматриваемый элемент - архив, распаковываем в подпапку папки archives, а сам архив удаляем
                    if key == 'archives':
                        shutil.unpack_archive(
                            i, str(Path(Path.cwd(), key, os.path.splitext(i.name)[0])))
                        os.remove(i)
                    # shutil требует на вход строку, так что конвертируем переданный адрес текущей директории в строку
                    else:
                        # проверка на случай дублирования файлов; если файл уже существует, удаляем его
                        try:
                            shutil.move(str(i), str(Path(Path.cwd(), key)))
                        except shutil.Error:
                            os.remove(i)


# ЗАПУСК ПРОГРАММЫ
# запуск основного метода, сканирующего целевую папку
dict_of_files, unknown_type_files, known_extension_types, unknown_extension_types = scan_directory(
    path)
# запуск метода, перемещающего файлы в целевую папку
move_files(path, dict_of_files)
# меняем в конце текущую директорию, чтобы закрыть папку с отсортированными файлами и ее можно было переместить или удалить
os.chdir('C:\\Users\\user\\Desktop')
