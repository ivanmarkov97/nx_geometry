from services.validators import ValidatorManager, PointValidator, LineValidator
from operators.nx_math import ver, hor, perpTwoLines, parTwoLines, eqTwoPoint
from operators.nx_math import Xc
from storage import Storage
from copy import copy
import json

def printer(data):
	print(data)
	return data


class CreateManager:
	@classmethod
	def create_point(cls, params):
		validator = PointValidator(params)
		if ValidatorManager.is_valid(validator):
			print("create point Operation")
			print(params)

			x_key = 'x_{}'.format(params['uid'])
			y_key = 'y_{}'.format(params['uid'])

			Xc[x_key] = params['point']['x']
			Xc[y_key] = params['point']['y']

			store_point = {'x': params['point']['x'], 'y': params['point']['y']}
			json_store_point = json.dumps(store_point)
			Storage.redis_db.set(params['uid'], json_store_point)

			print(Xc)
			return Xc
		else:
			raise ValueError('Usage point: {"uid":..., "point":{"x":..., "y":...}')


	@classmethod
	def create_line(cls, params):
		validator = LineValidator(params)
		if ValidatorManager.is_valid(validator):
			print("create_line Operation")
			print(params)

			try:
				x1_key = 'x_{}'.format(params['point1']['uid'])
				y1_key = 'y_{}'.format(params['point1']['uid'])

				x2_key = 'x_{}'.format(params['point2']['uid'])
				y2_key = 'y_{}'.format(params['point2']['uid'])

				Xc[x1_key] = params['point1']['x']
				Xc[y1_key] = params['point1']['y']
				Xc[x2_key] = params['point2']['x']
				Xc[y2_key] = params['point2']['y']

				store_line = {
					'point1': {
						'uid': params['point1']['uid'],
						'x': params['point1']['x'], 
						'y': params['point1']['y']
					},
					'point2': {
						'uid': params['point2']['uid'],
						'x': params['point2']['x'],
						'y': params['point2']['y']
					}
				}

				json_store_line = json.dumps(store_line)
				Storage.redis_db.set(params['uid'], json_store_line)

			except KeyError:
				raise KeyError('Usage line: {"uid":..., "point1":{"x", "y"}, "point2":{"x", "y"}')

			return Xc
		else:
			raise ValueError('Usage line: {"uid":..., "point1":{"uid", "x", "y"}, "point2":{"uid", "x", "y"}')


class RestrictionManager:
	@classmethod
	def vertical_strict(cls, data):
		print(data)
		line = Storage.redis_db.get(data['uid'])
		line = json.loads(line)

		id1 = line['point1']['uid']
		id2 = line['point2']['uid']
		solv_result = ver(id1, id2)

		try:
			store_line = {
				'point1': {
					'uid': line['point1']['uid'],
					'x': float(solv_result['x_'+line['point1']['uid']]), 
					'y': float(solv_result['y_'+line['point1']['uid']])
				},
				'point2': {
					'uid': line['point2']['uid'],
					'x': float(solv_result['x_'+line['point2']['uid']]), 
					'y': float(solv_result['y_'+line['point2']['uid']])
				}
			}

			json_store_line = json.dumps(store_line)
			Storage.redis_db.set(data['uid'], json_store_line)

		except KeyError:
				raise KeyError('Usage data: {"uid":...}')


	@classmethod
	def horizontal_strict(cls, data):
		print(data)
		line = Storage.redis_db.get(data['uid'])
		line = json.loads(line)

		id1 = line['point1']['uid']
		id2 = line['point2']['uid']
		solv_result = hor(id1, id2)

		try:
			store_line = {
				'point1': {
					'uid': line['point1']['uid'],
					'x': float(solv_result['x_'+line['point1']['uid']]), 
					'y': float(solv_result['y_'+line['point1']['uid']])
				},
				'point2': {
					'uid': line['point2']['uid'],
					'x': float(solv_result['x_'+line['point2']['uid']]), 
					'y': float(solv_result['y_'+line['point2']['uid']])
				}
			}

			json_store_line = json.dumps(store_line)
			Storage.redis_db.set(data['uid'], json_store_line)

		except KeyError:
				raise KeyError('Usage data: {"uid":...}')

	@classmethod
	def lines_perpendicular(cls, data):
		print(data)
		line1 = Storage.redis_db.get(data['uid1'])
		line1 = json.loads(line1)

		line2 = Storage.redis_db.get(data['uid2'])
		line2 = json.loads(line2)

		line1_id1 = line1['point1']['uid']
		line1_id2 = line1['point2']['uid']
		line2_id1 = line2['point1']['uid']
		line2_id2 = line2['point2']['uid']

		solv_result = perpTwoLines(line1_id1, line1_id2, line2_id1, line2_id2)
		print(solv_result)

		try:
			store_line1 = {
				'point1': {
					'uid': line1['point1']['uid'],
					'x': float(solv_result['x_'+line1['point1']['uid']]), 
					'y': float(solv_result['y_'+line1['point1']['uid']])
				},
				'point2': {
					'uid': line1['point2']['uid'],
					'x': float(solv_result['x_'+line1['point2']['uid']]), 
					'y': float(solv_result['y_'+line1['point2']['uid']])
				}
			}

			json_store_line1 = json.dumps(store_line1)
			Storage.redis_db.set(data['uid1'], json_store_line1)

			store_line2 = {
				'point1': {
					'uid': line2['point1']['uid'],
					'x': float(solv_result['x_'+line2['point1']['uid']]), 
					'y': float(solv_result['y_'+line2['point1']['uid']])
				},
				'point2': {
					'uid': line2['point2']['uid'],
					'x': float(solv_result['x_'+line2['point2']['uid']]), 
					'y': float(solv_result['y_'+line2['point2']['uid']])
				}
			}

			json_store_line2 = json.dumps(store_line2)
			Storage.redis_db.set(data['uid2'], json_store_line2)

		except KeyError:
				raise KeyError('Usage data: {"uid1":..., "uid2":...}')


	@classmethod
	def lines_parallel(cls, data):
		print("LINES PARALLEL")
		print(data)
		line1 = Storage.redis_db.get(data['uid1'])
		line1 = json.loads(line1)

		line2 = Storage.redis_db.get(data['uid2'])
		line2 = json.loads(line2)

		line1_id1 = line1['point1']['uid']
		line1_id2 = line1['point2']['uid']
		line2_id1 = line2['point1']['uid']
		line2_id2 = line2['point2']['uid']

		solv_result = parTwoLines(line1_id1, line1_id2, line2_id1, line2_id2)
		print(solv_result)

		try:
			store_line1 = {
				'point1': {
					'uid': line1['point1']['uid'],
					'x': float(solv_result['x_'+line1['point1']['uid']]), 
					'y': float(solv_result['y_'+line1['point1']['uid']])
				},
				'point2': {
					'uid': line1['point2']['uid'],
					'x': float(solv_result['x_'+line1['point2']['uid']]), 
					'y': float(solv_result['y_'+line1['point2']['uid']])
				}
			}

			json_store_line1 = json.dumps(store_line1)
			Storage.redis_db.set(data['uid1'], json_store_line1)

			store_line2 = {
				'point1': {
					'uid': line2['point1']['uid'],
					'x': float(solv_result['x_'+line2['point1']['uid']]), 
					'y': float(solv_result['y_'+line2['point1']['uid']])
				},
				'point2': {
					'uid': line2['point2']['uid'],
					'x': float(solv_result['x_'+line2['point2']['uid']]), 
					'y': float(solv_result['y_'+line2['point2']['uid']])
				}
			}

			json_store_line2 = json.dumps(store_line2)
			Storage.redis_db.set(data['uid2'], json_store_line2)

		except KeyError:
				raise KeyError('Usage data: {"uid1":..., "uid2":...}')


	@classmethod
	def connect_points(cls, data):
		print("CONNECT POINTS")
		print(data)

		object1 = Storage.redis_db.get(data['point1']['uid'])
		object1 = json.loads(object1)

		object2 = Storage.redis_db.get(data['point2']['uid'])
		object2 = json.loads(object2)

		if data['point1']['pointNum'] is None:
			id1 = data['point1']['uid']
			object1['type'] = 'Point'
		else:
			point_key = 'point{}'.format(data['point1']['pointNum'])
			id1 = object1[point_key]['uid']
			object1['type'] = 'Line'

		if data['point2']['pointNum'] is None:
			id2 = data['point2']['uid']
			object2['type'] = 'Point'
		else:
			point_key = 'point{}'.format(data['point2']['pointNum'])
			id2 = object2[point_key]['uid']
			object2['type'] = 'Line'

		print(object1)
		print(object2)
		print(id1, id2)

		solv_result = eqTwoPoint(id1, id2)
		print(solv_result)

		if object1['type'] == 'Point':
			store_point = {
				'x': float(solv_result['x_'+data['point1']['uid']]), 
				'y': float(solv_result['y_'+data['point1']['uid']])
			}
			json_store_point = json.dumps(store_point)
			Storage.redis_db.set(data['point1']['uid'], json_store_point)
			del object1['type']
		elif object1['type'] == 'Line':
			if int(data['point1']['pointNum']) == 1:
				store_line = {
					'point1': {
						'uid': object1['point1']['uid'],
						'x': float(solv_result['x_'+object1['point1']['uid']]), 
						'y': float(solv_result['y_'+object1['point1']['uid']])
					},
					'point2': {
						'uid': object1['point2']['uid'],
						'x': object1['point2']['x'], 
						'y': object1['point2']['y']
					}
				}
			else:
				store_line = {
					'point1': {
						'uid': object1['point1']['uid'],
						'x': object1['point1']['x'],
						'y': object1['point1']['y']
					},
					'point2': {
						'uid': object1['point2']['uid'],
						'x': float(solv_result['x_'+object1['point2']['uid']]),
						'y': float(solv_result['y_'+object1['point2']['uid']])
					}
				}

			del object1['type']
			json_store_line = json.dumps(store_line)
			Storage.redis_db.set(data['point1']['uid'], json_store_line)

		if object2['type'] == 'Point':
			store_point = {
				'x': float(solv_result['x_'+data['point2']['uid']]), 
				'y': float(solv_result['y_'+data['point2']['uid']])
			}
			json_store_point = json.dumps(store_point)
			Storage.redis_db.set(data['point2']['uid'], json_store_point)
			del object2['type']
		elif object2['type'] == 'Line':
			if int(data['point2']['pointNum']) == 1:
				store_line = {
					'point1': {
						'uid': object2['point1']['uid'],
						'x': float(solv_result['x_'+object2['point1']['uid']]), 
						'y': float(solv_result['y_'+object2['point1']['uid']])
					},
					'point2': {
						'uid': object2['point2']['uid'],
						'x': object2['point2']['x'], 
						'y': object2['point2']['y']
					}
				}
			else:
				store_line = {
					'point1': {
						'uid': object2['point1']['uid'],
						'x': object2['point1']['x'],
						'y': object2['point1']['y']
					},
					'point2': {
						'uid': object2['point2']['uid'],
						'x': float(solv_result['x_'+object2['point2']['uid']]),
						'y': float(solv_result['y_'+object2['point2']['uid']])
					}
				}

			del object2['type']
			json_store_line = json.dumps(store_line)
			Storage.redis_db.set(data['point2']['uid'], json_store_line)

	@classmethod
	def attach_point_to_line(cls, data):
		print("ATTACH POINT TO LINE")
		print(data)

		point = Storage.redis_db.get(data['uid1'])
		point = json.loads(point)

		line = Storage.redis_db.get(data['uid2'])
		line = json.loads(line)



class DragManager:
	@classmethod
	def drag_point(cls, data):
		pass

	@classmethod
	def drag_line(cls, data):
		pass
