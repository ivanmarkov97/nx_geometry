from functools import wraps
import json

def data_parser(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		json_data = json.loads(args[0])
		try:
			operation = json_data['operation']
			data = json_data['data']
			return f(data, operation).encode('utf-8')
		except KeyError:
			raise KeyError('Invalid input data. Usage: {"operation": ..., "data": ...}')
	return wrapper
