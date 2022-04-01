import os
from pathlib import Path
from clean_folder_my_version.secondary_methods import normalize, handle_duplicates, handle_unknown, handle_archives
from clean_folder_my_version.data import extens_types, unknown_files, known_extens, unknown_extens, lists_of_files

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

    return unknown_files, known_extens, unknown_extens, lists_of_files

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


# метод для вывода списков файлов и расширений


def print_results(unknown_files, known_extens, unknown_extens, lists_of_files):
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
