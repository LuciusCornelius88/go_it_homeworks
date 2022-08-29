import functools


class UnhashableType(Exception):
	...


class LruCache:

	def __init__(self, client, max_size, cache, queue):
		self.client = client
		self.max_size = max_size
		self.cache = cache
		self.queue = queue
		self.key_prefix = 'LRU_cache'
		self.pipeline = self.client.pipeline()
		self.pipeline.multi()

		self.cache_info_sample = {
								'hits': 0, 
								'misses': 0, 
								'maxsize': self.max_size, 
								'currsize': 0
							}

	def push_new_elem(self, new_key, new_elem):

		self.client.hset(self.cache, new_key, new_elem)
		self.client.lpush(self.queue, new_key)
		self.pipeline.execute(raise_on_error=True)

		print(f'New key {new_key} was added to cache!')


	def push_delete_elem(self, new_key, new_elem):
		
		last_elem = self.client.lindex(self.queue, -1)

		self.client.hdel(self.cache, last_elem)
		self.client.hset(self.cache, new_key, new_elem)
		
		self.client.lrem(self.queue, -1, last_elem)
		self.client.lpush(self.queue, new_key)

		self.pipeline.execute(raise_on_error=True)

		print(f'Key {last_elem} was replaced by the new key {new_key} in cache!')


	def move_elem(self, key):

		self.client.lrem(self.queue, 1, key)
		self.client.lpush(self.queue, key)
		self.pipeline.execute(raise_on_error=True)

		print(f'Key {key} was set on the top of queue!')


	def key_hasher(self, return_type, func, *args, **kwargs):

		try:
			hashed_args = tuple([hash(arg) for arg in args])
			hashed_kwargs = tuple([hash(arg) for arg in kwargs.values()])
		except TypeError:
			raise UnhashableType

		return '{}:{}:{}{!r}:{!r}:{}'.format(self.key_prefix, func.__module__, func.__qualname__, 
										  hashed_args, hashed_kwargs, return_type)


	def cache_info(self):
		return self.cache_info_sample


	def clear_cache(self):
		for key in list(self.client.hgetall(self.cache).keys()):
			self.client.hdel(self.cache, key)
			self.client.lrem(self.queue, 1, key)
		self.pipeline.execute(raise_on_error=True)
		self.cache_info_sample['hits'] = 0
		self.cache_info_sample['misses'] = 0
		self.cache_info_sample['currsize'] = 0

		print('Cache is empty!')


	def __call__(self, func):

		@functools.wraps(func)
		def inner(*args, **kwargs):
			try:
				return_type = func.__annotations__.get('return')
				if return_type:
					return_type = return_type.__qualname__
				key = self.key_hasher(return_type, func, *args, **kwargs) 
			except UnhashableType:
				self.cache_info_sample['misses'] += 1
				return func(*args, **kwargs)
			else:
				try:
					result = self[key]
					self.move_elem(key)
					self.cache_info_sample['hits'] += 1
					return result
				except KeyError:
					result = func(*args, **kwargs)
					if self.max_size and len(self.cache) == self.max_size:
						self.push_delete_elem(key, result)
					else:
						self.push_new_elem(key, result)
					self.cache_info_sample['misses'] += 1
					self.cache_info_sample['currsize'] += 1
					return result
		return inner

	# при преобразовании типа стоит костыляка, т.к. корректно работает только в случае, 
	# если у функции есть аннотация возвращаемого значения
	def __getitem__(self, key):
		if self.client.hexists(self.cache, key):
			return_type = eval(key.split(':')[-1])
			return_value = self.client.hget(self.cache, key)
			return return_type(return_value) if return_type else int(return_value)
		else:
			raise KeyError