from uuid import uuid4
from math import sqrt

class BasePrimitive:
	def __init__(self, uid=None):
		self._uid = uid if uid is not None else str(uuid4())

	@property
	def uid(self):
		return self._uid
		

class Point(BasePrimitive):
	def __init__(self, coords, uid=None):
		self.x, self.y = coords
		super().__init__(uid)


class Line(BasePrimitive):
	def __init__(self, p1, p2, uid=None):
		self.points = [p1, p2]
		super().__init__(uid)

	def point_by_uid(self, uuid):
		return filter(lambda p: p.uid == uid, self.points)[0]

	@property
	def length(self):
		return sqrt(
			(self.points[0].x - self.points[1].x)**2 + 
			(self.points[0].y - self.points[1].y)**2
			)
