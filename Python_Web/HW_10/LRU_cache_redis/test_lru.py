import redis
from lru_redis import LruCache

client = redis.Redis(host='localhost', port=6379, db=0) # charset='utf-8', decode_responses=True

client.flushdb()

CACHE_NAME = 'my_cache'
QUEUE_NAME = 'my_queue'

MAX_LENGTH = 10

my_cache = LruCache(client, MAX_LENGTH, CACHE_NAME, QUEUE_NAME)


@my_cache
def fib(n) -> int:
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


if __name__ == '__main__':
	print('\n')
	print([fib(n) for n in range(16)])
	print('\n')
	print(my_cache.cache_info())

	

	