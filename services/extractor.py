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


def stored_single_line(f):
	# for class usage (self | cls)
	@wraps(f)
	def wrapper(*args, **kwargs):
		print("stored_single_line")
		data = args[1]
		line = Storage.redis_db.get(data['uid'])
		line = json.loads(line)
		point1_uid = line['point1']['uid']
		point2_uid = line['point2']['uid']

		# args[0] ~ self | cls
		result = f(args[0], data['uid'], point1_uid, point2_uid)
		solv_result = result['data']
		restriction_name = result['restriction']

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

			return {
				'line_uid': data['uid'], 
				'restriction': restriction_name,
			 	'args': [point1_uid, point2_uid]
			 }
		except KeyError:
			raise KeyError('Usage data: {"uid":...}')
	return wrapper


def stored_line_restriction(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		print("stored_line_restriction")
		data = f(*args, **kwargs)
		restrictions = Storage.get_restiction_for_object(data['line_uid'])
		if restrictions is not None:
			restrictions[data['line_uid']].append({'name': data['restriction'], 'args': data['args']})
		else:
			restrictions = {data['line_uid']: [{'name': data['restriction'], 'args': data['args']}]}
		Storage.set_restrictions(restrictions)
	return wrapper


def stored_two_lines(f):
	# for class usage (self | cls)
	@wraps(f)
	def wrapper(*args, **kwargs):
		data = args[1]
		line1 = Storage.redis_db.get(data['uid1'])
		line1 = json.loads(line1)

		line2 = Storage.redis_db.get(data['uid2'])
		line2 = json.loads(line2)

		line1_point_uid1 = line1['point1']['uid']
		line1_point_uid2 = line1['point2']['uid']
		line2_point_uid1 = line2['point1']['uid']
		line2_point_uid2 = line2['point2']['uid']

		# args[0] ~ self | cls
		solv_result = f(args[0], data['uid1'], data['uid1'], 
			line1_point_uid1, line1_point_uid2, line2_point_uid1, line2_point_uid2)

		try:
			store_line1 = {
				'point1': {
					'uid': line1_point_uid1,
					'x': float(solv_result['x_'+line1_point_id1]), 
					'y': float(solv_result['y_'+line1_point_id1])
				},
				'point2': {
					'uid': line1_point_uid2,
					'x': float(solv_result['x_'+line1_point_id2]), 
					'y': float(solv_result['y_'+line1_point_id2])
				}
			}

			json_store_line1 = json.dumps(store_line1)
			Storage.redis_db.set(data['uid1'], json_store_line1)

			store_line2 = {
				'point1': {
					'uid': line2_point_uid1,
					'x': float(solv_result['x_'+line2_point_id1]), 
					'y': float(solv_result['y_'+line2_point_id1])
				},
				'point2': {
					'uid': line2_point_uid2,
					'x': float(solv_result['x_'+line2_point_id2]), 
					'y': float(solv_result['y_'+line2_point_id2])
				}
			}

			json_store_line2 = json.dumps(store_line2)
			Storage.redis_db.set(data['uid2'], json_store_line2)

		except KeyError:
				raise KeyError('Usage data: {"uid1":..., "uid2":...}')

	return wrapper

