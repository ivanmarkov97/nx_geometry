from storage import Storage
from functools import wraps
import json

def data_parser(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		json_data = json.loads(args[0])
		try:
			operation = json_data['operation']
			data = json_data['data']
			return str(f(data, operation))
		except KeyError:
			raise KeyError('Invalid input data. Usage: {"operation": ..., "data": ...}')
	return wrapper


def stored_line(f):
	"""
	for class usage (self | cls)
	"""
	@wraps(f)
	def wrapper(*args, **kwargs):
		data = args[1]
		line = Storage.redis_db.get(data['uid'])
		line = json.loads(line)
		point1_uid = line['point1']['uid']
		point2_uid = line['point2']['uid']

		# args[0] ~ self | cls
		solv_result = f(args[0], data['uid'], point1_uid, point2_uid)
		try:
			store_line = {
				'point1': {
					'uid': line['point1']['uid'],
					'x': float(solv_result['x_'+point1_uid]), 
					'y': float(solv_result['y_'+point1_uid])
				},
				'point2': {
					'uid': line['point2']['uid'],
					'x': float(solv_result['x_'+point2_uid]), 
					'y': float(solv_result['y_'+point2_uid])
				}
			}

			json_store_line = json.dumps(store_line)
			Storage.redis_db.set(data['uid'], json_store_line)

		except KeyError:
				raise KeyError('Usage data: {"uid":...}')
	return wrapper
