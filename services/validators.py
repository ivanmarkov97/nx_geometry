class BaseValidator:
	def __init__(self, data):
		self.data = data

	def is_valid(self) -> bool:
		raise NotImplementedError('Not Implemented abstract method for BaseValidator')

	def validate_uid(self):
		return 'uid' in self.data.keys()


class PointValidator(BaseValidator):
	# тупо но для начала пойдет
	def validate_data_size(self) -> bool:
		return len(self.data) == 2

	def validate_point_exist(self) -> bool:
		return 'point' in self.data.keys()

	def validate_point_size(self) -> bool:
		try:
			return len(self.data['point']) == 2
		except KeyError:
			return False

	def validate_point_items(self) -> bool:
		try:
			return len(set(['x', 'y']) & set(self.data['point'].keys())) == 2
		except KeyError:
			return False


class LineValidator(BaseValidator):

	def validate_data_size(self) -> bool:
		return len(self.data) == 3

	def validate_points_exist(self) -> bool:
		return len(set(['point1', 'point2']) & set(self.data.keys())) == 2

	def validate_point1_items(self) -> bool:
		try:
			return len(set(['uid', 'x', 'y']) & set(self.data['point1'].keys())) == 3
		except KeyError:
			print("Incorrect validate pint1 items")
			return False

	def validate_point2_items(self) -> bool:
		try:
			return len(set(['uid', 'x', 'y']) & set(self.data['point2'].keys())) == 3
		except KeyError:
			print("Incorrect validate pint2 items")
			return False


class ValidatorManager:
	@classmethod
	def is_valid(self, obj):
		methods_to_call = list(filter(lambda x: x.startswith('validate_'), dir(obj)))
		total_check = {getattr(obj, method)() for method in methods_to_call}
		print(total_check)
		return False not in total_check
