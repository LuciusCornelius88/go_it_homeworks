import time
import sys
from multiprocessing import Process, Manager
from datetime import timedelta


def factorize(lst, num: int):
    for i in range(1, num+1):
        if num % i == 0:
            lst.append(i)
    
    sys.exit(0)


if __name__ == '__main__':
    start_time = time.monotonic()

    nums_lst = [128, 255, 99999, 10651060]
    processes = []
    
    manager = Manager()
    man_lst = manager.list()
    
    for _ in range(len(nums_lst)):
        man_lst.append(manager.list())

    for i in range(len(nums_lst)):
        new_process = Process(target=factorize, args=(man_lst[i], nums_lst[i]))
        new_process.start()
        processes.append(new_process)

    [process.join() for process in processes]

    end_time = time.monotonic()
    print(f'Time of execution: {timedelta(seconds=end_time - start_time)}')

    for lst in man_lst:
        print(lst)