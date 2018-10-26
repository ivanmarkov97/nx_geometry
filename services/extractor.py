from functools import wraps
import json

def data_parser(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		json_data = json.loads(args[0])
		print("JSON DATA")
		print(json_data)
		try:
			operation = json_data['operation']
			data = json_data['data']
			return str(f(data, operation))
		except KeyError:
			raise KeyError('Invalid input data. Usage: {"operation": ..., "data": ...}')
	return wrapper
