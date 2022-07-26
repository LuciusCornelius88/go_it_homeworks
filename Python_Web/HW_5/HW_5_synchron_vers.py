import time
from datetime import timedelta

def factorize(num: int):
    lst = []
    
    for i in range(1, num+1):
        if num % i == 0:
            lst.append(i)
                
    return lst


start_time = time.monotonic()

nums_lst = [128, 255, 99999, 10651060]
results = []

for num in nums_lst:
    result = factorize(num)
    results.append(result)

end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))

print(results)