from services.validators import ValidatorManager, PointValidator, LineValidator
from operators.nx_math import ver, hor
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