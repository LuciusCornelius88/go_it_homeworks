import asyncio
import time
import functools
from pathlib import Path
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


async def main():
    dirpath = get_dirpath()

    start = time.time()

    main_dir = MainDirectory(dirpath)

    start_scan = time.time()
    print('start scanning')
    await main_dir.scan_directory()
    print(f'stop scanning: {time.time() - start_scan}')

    start_handl = time.time()
    print('start handling dirs and files')
    await asyncio.gather(main_dir.create_directories(),
                         main_dir.delete_directories(),
                         main_dir.classify_files())
    print(f'stop handling dirs and files: {time.time() - start_handl}')

    start_sort = time.time()
    print('start sorting')
    await asyncio.gather(main_dir.sort_files(),
                         main_dir.represent_sorted_files())
    print(f'stop sorting: {time.time() - start_sort}')

    print(f'Total time: {time.time() - start}')


if __name__ == '__main__':
    asyncio.run(main())
