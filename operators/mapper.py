from .operations import printer

mapped_operations = [
	('create_point', None),
	('create_line', None),

	('drag_point', None),
	('drag_line', None),

	('horizontal', None),
	('vertical', None),
	('parallel', None),
	('perpendicular', None),

	('connect_points', None), 

	('attache_point_to_line', None),
	('angle_between_lines', None),
	
	('distz_between_points', None),

	('test', printer)
]
