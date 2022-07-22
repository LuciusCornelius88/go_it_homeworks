import functools
from pathlib import Path
from threading import Thread
from main_directory_classes import MainDirectory


def correct_path_check(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        dirpath = func()
        if dirpath.exists() and dirpath.is_dir():
            return dirpath
        else:
            print('Path does not ecxist or is not a directory!')
            return inner(*args, **kwargs)
    return inner


@correct_path_check
def get_dirpath():
    dirpath = Path(input('Please, enter path to directory: '))
    return dirpath


def main():
    dirpath = get_dirpath()
    main_dir = MainDirectory(dirpath)
    thread_1 = Thread(target=main_dir.scan_directory)
    thread_2 = Thread(target=main_dir.create_directories)
    thread_3 = Thread(target=main_dir.delete_directories)
    thread_4 = Thread(target=main_dir.classify_files)
    thread_5 = Thread(target=main_dir.sort_files)
    thread_6 = Thread(target=main_dir.represent_sorted_files)

    thread_1.start()
    thread_1.join()

    thread_2.start()
    thread_3.start()
    thread_2.join()
    thread_3.join()

    thread_4.start()
    thread_4.join()

    thread_5.start()
    thread_6.start()


if __name__ == '__main__':
    main()
