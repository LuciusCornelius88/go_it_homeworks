import time
from multiprocessing import Process, Pool
from datetime import timedelta


def factorize(num: int):
    lst = []
    
    for i in range(1, num+1):
        if num % i == 0:
            lst.append(i)
                
    return lst


if __name__ == '__main__':
	start_time = time.monotonic()

	lst = [128, 255, 99999, 10651060]

	with Pool(processes=4) as pool:
		result = pool.map(factorize, lst)

	end_time = time.monotonic()
	print(f'Time of execution: {timedelta(seconds=end_time - start_time)}')

	print(result)

	# a, b, c, d = result

	# end_time = time.monotonic()
	# print(f'Tiem of execution: {timedelta(seconds=end_time - start_time)}')

	# print(a == [1, 2, 4, 8, 16, 32, 64, 128])
	# print(b == [1, 3, 5, 15, 17, 51, 85, 255])
	# print(c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999])
	# print(d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 
	# 	  		760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060])
