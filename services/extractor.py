from storage import Storage
from functools import wraps
import json


def find_new_values_for_point(point_uid, solv_result):
	point_x_value = None; point_y_value = None

	for xy_point_uid in solv_result:
		if xy_point_uid[1:] == point_uid:
			if xy_point_uid.startswith('x'):
				point_x_value = solv_result[xy_point_uid]
			elif xy_point_uid.startswith('y'):
				point_y_value = solv_result[xy_point_uid]

	return point_x_value, point_y_value


def find_new_values_for_line_points(point1_uid, point2_uid, solv_result):
	point1_x_value = None; point1_y_value = None
	point2_x_value = None; point2_y_value = None

	for xy_point_uid in solv_result:
		if xy_point_uid[1:] == point1_uid:
			if xy_point_uid.startswith('x'):
				point1_x_value = solv_result[xy_point_uid]
			elif xy_point_uid.startswith('y'):
				point1_y_value = solv_result[xy_point_uid]

	for xy_point_uid in solv_result:
		if xy_point_uid[1:] == point2_uid:
			if xy_point_uid.startswith('x'):
				point2_x_value = solv_result[xy_point_uid]
			elif xy_point_uid.startswith('y'):
				point2_y_value = solv_result[xy_point_uid]

	return point1_x_value, point1_y_value, point2_x_value, point2_y_value



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

		print("SOLV RESULT")
		print(solv_result)

		try:
			store_line = {
				'point1': {
					'uid': line['point1']['uid'],
					'x': float(solv_result['x'+point1_uid]), 
					'y': float(solv_result['y'+point1_uid])
				},
				'point2': {
					'uid': line['point2']['uid'],
					'x': float(solv_result['x'+point2_uid]), 
					'y': float(solv_result['y'+point2_uid])
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


def stored_drag_line(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		print('drag')
		data = args[1]

		line = Storage.redis_db.get(data['uid'])
		line = json.loads(line)
		print("LINE :", line)

		pos_new = {
			data['point1']['uid']: data['point1'],
			data['point2']['uid']: data['point2']
		}

		solv_result = f(args[0], pos_new, **kwargs)['data']

		print('solv_result')
		print(solv_result)

		all_storage = Storage.export_all_data_native()

		for storage_object in all_storage:
			storage_object_key = list(storage_object.keys())[0]
			storage_object[storage_object_key] = json.loads(storage_object[storage_object_key])
			if 'point1' in storage_object[storage_object_key]:
				"""
				this is line
				"""
				point1_uid = storage_object[storage_object_key]['point1']['uid']
				point2_uid = storage_object[storage_object_key]['point2']['uid']

				point1_x_value, point1_y_value,\
				point2_x_value, point2_y_value = find_new_values_for_line_points(point1_uid, point2_uid, solv_result)

				store_line = {
					'point1': {
						'uid': point1_uid,
						'x': point1_x_value,
						'y': point1_y_value
					},
					'point2': {
						'uid': point2_uid,
						'x': point2_x_value,
						'y': point2_y_value
					}
				}
				json_store_line = json.dumps(store_line)
				Storage.redis_db.set(storage_object_key, json_store_line)
			elif 'x' in storage_object[storage_object_key]:
				"""
				this is point
				"""
				point_x_value, point_y_value = find_new_values_for_point(storage_object_key, solv_result)

				store_point = {
					'x': point_x_value,
					'y': point_y_value
				}
				json_store_point = json.dumps(store_point)
				Storage.redis_db.set(storage_object_key, json_store_point)
		return {}

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

		print("LINE 1:", line1)
		print("LINE 2:", line2)

		line1_point_uid1 = line1['point1']['uid']
		line1_point_uid2 = line1['point2']['uid']
		line2_point_uid1 = line2['point1']['uid']
		line2_point_uid2 = line2['point2']['uid']

		if 'angle' in data.keys():
			kwargs['angle'] = data['angle']

		# args[0] ~ self | cls
		result = f(args[0], data['uid1'], data['uid1'], 
			line1_point_uid1, line1_point_uid2, line2_point_uid1, line2_point_uid2, **kwargs)
		solv_result = result['data']

		print("SOLVE RESULT", solv_result)

		restriction_name = result['restriction']

		try:
			store_line1 = {
				'point1': {
					'uid': line1_point_uid1,
					'x': float(solv_result['x'+line1_point_uid1]), 
					'y': float(solv_result['y'+line1_point_uid1])
				},
				'point2': {
					'uid': line1_point_uid2,
					'x': float(solv_result['x'+line1_point_uid2]), 
					'y': float(solv_result['y'+line1_point_uid2])
				}
			}
			store_line2 = {
				'point1': {
					'uid': line2_point_uid1,
					'x': float(solv_result['x'+line2_point_uid1]), 
					'y': float(solv_result['y'+line2_point_uid1])
				},
				'point2': {
					'uid': line2_point_uid2,
					'x': float(solv_result['x'+line2_point_uid2]), 
					'y': float(solv_result['y'+line2_point_uid2])
				}
			}

			json_store_line1 = json.dumps(store_line1)
			Storage.redis_db.set(data['uid1'], json_store_line1)
			
			json_store_line2 = json.dumps(store_line2)
			Storage.redis_db.set(data['uid2'], json_store_line2)

			return {
				#'line_uid': data['uid'], 
				#'restriction': restriction_name,
			 	#'args': [point1_uid, point2_uid]
			 }

		except KeyError:
			raise KeyError('Usage data: {"uid1":..., "uid2":...}')
	return wrapper


def stored_distance(f):
	# for class usage (self | cls)
	@wraps(f)
	def wrapper(*args, **kwargs):
		data = args[1]
		print("######DATA##### distance")
		print(args, kwargs)

		object1 = None
		object2 = None

		print("DATA: ", data)

		if data['point1']['parent'] is not None:
			#print("THIS IS POINT {} FROM LINE {}".format(data['point1']['pointNum'], data['point1']['parent']))
			object1 = Storage.redis_db.get(data['point1']['parent'])
			object1 = json.loads(object1)
			point_key = 'point{}'.format(data['point1']['pointNum']) 
			id1 = object1[point_key]['uid']
			object1['type'] = 'Line'
		elif data['point1']['uid'] in Storage.redis_db.keys():
			#print("THIS IS POINT")
			object1 = Storage.redis_db.get(data['point1']['uid'])
			object1 = json.loads(object1)
			id1 = data['point1']['uid']
			object1['type'] = 'Point'
		else:
			raise ValueError("OBJECT DOESNT EXIST")

		if data['point2']['parent'] is not None:
			#print("THIS IS POINT {} FROM LINE {}".format(data['point1']['pointNum'], data['point1']['parent']))
			object2 = Storage.redis_db.get(data['point2']['parent'])
			object2 = json.loads(object2)
			point_key = 'point{}'.format(data['point2']['pointNum']) 
			id2 = object2[point_key]['uid']
			object2['type'] = 'Line'
		elif data['point1']['uid'] in Storage.redis_db.keys():
			#print("THIS IS POINT")
			object2 = Storage.redis_db.get(data['point2']['uid'])
			object2 = json.loads(object2)
			id2 = data['point2']['uid']
			object2['type'] = 'Point'
		else:
			raise ValueError("OBJECT DOESNT EXIST")

		print('pbject1 ', object1)
		print('object2 ', object2)
		print('data ', data)
		print(id1, id2)

		if 'distance' in data:	
			result = f(args[0], data['distance'], id1, id2)
		else:
			result = f(args[0], id1, id2)
		print("SOLVE RESULT")
		print(result)

		solv_result = result['data']
		
		if object1['type'] == 'Point':
			store_point = {
				'x': float(solv_result['x'+data['point1']['uid']]), 
				'y': float(solv_result['y'+data['point1']['uid']])
			}
			json_store_point = json.dumps(store_point)
			Storage.redis_db.set(data['point1']['uid'], json_store_point)
			del object1['type']
		elif object1['type'] == 'Line':
			if int(data['point1']['pointNum']) == 1:
				store_line = {
					'point1': {
						'uid': object1['point1']['uid'],
						'x': float(solv_result['x'+object1['point1']['uid']]), 
						'y': float(solv_result['y'+object1['point1']['uid']])
					},
					'point2': {
						'uid': object1['point2']['uid'],
						'x': object1['point2']['x'], 
						'y': object1['point2']['y']
					}
				}
			elif int(data['point1']['pointNum']) == 2:
				store_line = {
					'point1': {
						'uid': object1['point1']['uid'],
						'x': object1['point1']['x'],
						'y': object1['point1']['y']
					},
					'point2': {
						'uid': object1['point2']['uid'],
						'x': float(solv_result['x'+object1['point2']['uid']]),
						'y': float(solv_result['y'+object1['point2']['uid']])
					}
				}

			del object1['type']
			json_store_line = json.dumps(store_line)
			Storage.redis_db.set(data['point1']['parent'], json_store_line)

		if object2['type'] == 'Point':
			store_point = {
				'x': float(solv_result['x'+data['point2']['uid']]), 
				'y': float(solv_result['y'+data['point2']['uid']])
			}
			json_store_point = json.dumps(store_point)
			Storage.redis_db.set(data['point2']['uid'], json_store_point)
			del object2['type']
		elif object2['type'] == 'Line':
			if int(data['point2']['pointNum']) == 1:
				store_line = {
					'point1': {
						'uid': object2['point1']['uid'],
						'x': float(solv_result['x'+object2['point1']['uid']]), 
						'y': float(solv_result['y'+object2['point1']['uid']])
					},
					'point2': {
						'uid': object2['point2']['uid'],
						'x': object2['point2']['x'], 
						'y': object2['point2']['y']
					}
				}
			elif int(data['point2']['pointNum']) == 2:
				store_line = {
					'point1': {
						'uid': object2['point1']['uid'],
						'x': object2['point1']['x'],
						'y': object2['point1']['y']
					},
					'point2': {
						'uid': object2['point2']['uid'],
						'x': float(solv_result['x'+object2['point2']['uid']]),
						'y': float(solv_result['y'+object2['point2']['uid']])
					}
				}

			del object2['type']
			json_store_line = json.dumps(store_line)
			Storage.redis_db.set(data['point2']['parent'], json_store_line)
	return wrapper

