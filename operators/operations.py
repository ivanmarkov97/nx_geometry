from services.validators import ValidatorManager, PointValidator, LineValidator
from services.extractor import (stored_single_line, 
								stored_two_lines,
								stored_distance,
								stored_line_restriction)
from operators.nx_math import Xc
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
		solv_result = nx_math.angleTwoLines(90.0, *points)
		return {'data': solv_result, 'restriction': nx_math.angleTwoLines.__name__}


	@classmethod
	@stored_two_lines
	def lines_parallel(cls, line1_uid, line2_uid, *points):
		solv_result = nx_math.angleTwoLines(0.0, *points)
		return {'data': solv_result, 'restriction': nx_math.angleTwoLines.__name__}


	@classmethod
	@stored_distance
	def connect_points(cls, *ids):
		print("CONNECT POINTS")
		solv_result = nx_math.eqTwoPoint(*ids)
		print("SOLVE RESULT")
		print(solv_result)
		return {'data': solv_result, 'restriction': nx_math.eqTwoPoint.__name__}


	@classmethod
	def attach_point_to_line(cls, data):
		print("ATTACH POINT TO LINE")
		print(data)

		point = Storage.redis_db.get(data['uid1'])
		point = json.loads(point)

		line = Storage.redis_db.get(data['uid2'])
		line = json.loads(line)


class ToolManager:
	@classmethod
	@stored_two_lines
	def angle_between_lines(cls, line1_uid, line2_uid, *points, **kwargs): # points: point uids, kwargs: {'angle': 60}
		solv_result = nx_math.angleTwoLines(kwargs['angle'], *points)
		print("SOLVE RESULT")
		print(solv_result)
		return {'data': solv_result, 'restriction': nx_math.angleTwoLines.__name__}

	@classmethod
	@stored_distance
	def distTwoPoint(cls, distance, *ids):
		print("DISTANCE BETWEEN POINTS")
		solv_result = nx_math.distTwoPoint(distance, *ids)
		print("SOLVE RESULT")
		print(solv_result)
		return {'data': solv_result, 'restriction': nx_math.distTwoPoint.__name__}
