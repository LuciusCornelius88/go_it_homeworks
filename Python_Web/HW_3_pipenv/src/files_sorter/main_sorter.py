import functools
from pathlib import Path
from files_sorter.main_directory_classes import MainDirectory


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
    main_dir.scan_directory()
    main_dir.create_directories()
    main_dir.delete_directories()
    main_dir.classify_files()
    main_dir.sort_files()
    main_dir.represent_sorted_files()


# if __name__ == '__main__':
#     main()
