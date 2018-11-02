from services.validators import ValidatorManager, PointValidator, LineValidator
from services.extractor import (stored_single_line, 
								stored_two_lines,
								stored_line_restriction)
from operators.nx_math import Xc
#from operators.nx_math import ver, hor, perpTwoLines, parTwoLines, eqTwoPoint
from operators import nx_math
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
			x_key = 'x{}'.format(params['uid'])
			y_key = 'y{}'.format(params['uid'])

			Xc[x_key] = params['point']['x']
			Xc[y_key] = params['point']['y']

			store_point = {'x': params['point']['x'], 'y': params['point']['y']}
			json_store_point = json.dumps(store_point)
			Storage.redis_db.set(params['uid'], json_store_point)
			return Xc
		else:
			raise ValueError('Usage point: {"uid":..., "point":{"x":..., "y":...}')


	@classmethod
	def create_line(cls, params):
		validator = LineValidator(params)
		if ValidatorManager.is_valid(validator):
			try:
				x1_key = 'x{}'.format(params['point1']['uid'])
				y1_key = 'y{}'.format(params['point1']['uid'])

				x2_key = 'x{}'.format(params['point2']['uid'])
				y2_key = 'y{}'.format(params['point2']['uid'])

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
	@stored_line_restriction
	@stored_single_line
	def vertical_strict(cls, line_uid, *points):
		print("vertical_strict")
		solv_result = nx_math.ver(*points)
		return {'data': solv_result, 'restriction': nx_math.ver.__name__}


	@classmethod
	@stored_line_restriction
	@stored_single_line
	def horizontal_strict(cls, line_uid, *points):
		solv_result = nx_math.hor(*points)
		return {'data': solv_result, 'restriction': nx_math.hor.__name__}


	@classmethod
	@stored_two_lines
	def lines_perpendicular(cls, line1_uid, line2_uid, *points):
		solv_result = nx_math.perpTwoLines(*points)
		return {'data': solv_result, 'restriction': nx_math.perpTwoLines.__name__}


	@classmethod
	@stored_two_lines
	def lines_parallel(cls, line1_uid, line2_uid, *points):
		solv_result = nx_math.parTwoLines(*points)
		return {'data': solv_result, 'restriction': nx_math.parTwoLines.__name__}


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

		solv_result = nx_math.eqTwoPoint(id1, id2)
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

class ToolManager:
	@classmethod
	@stored_two_lines
	def angle_between_lines(cls, line1_uid, line2_uid, *points, **kwargs): # points: point uids, kwargs: {'angle': 60}
		print("ARGS", points, kwargs)
		solv_result = nx_math.angleTwoLines(kwargs['angle'], *points)
		print("SOLVE RESULT")
		print(solv_result)
		return {'data': solv_result, 'restriction': nx_math.angleTwoLines.__name__}
