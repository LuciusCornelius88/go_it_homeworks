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
    
    manager = Manager()
    man_lst = manager.list()
    
    for _ in range(len(nums_lst)):
        man_lst.append(manager.list())

    process_1 = Process(target=factorize, args=(man_lst[0], nums_lst[0]))
    process_2 = Process(target=factorize, args=(man_lst[1], nums_lst[1]))
    process_3 = Process(target=factorize, args=(man_lst[2], nums_lst[2]))
    process_4 = Process(target=factorize, args=(man_lst[3], nums_lst[3]))

    process_1.start()
    process_2.start()
    process_3.start()
    process_4.start()
        
    process_1.join()
    process_2.join()
    process_3.join()
    process_4.join()

    end_time = time.monotonic()
    print(f'Time of execution: {timedelta(seconds=end_time - start_time)}')

    for lst in man_lst:
        print(lst)