from .operations import printer, CreateManager, RestrictionManager, ToolManager
from .nx_math import (distTwoPoint,
					  eqTwoPoint,
					  perpTwoLines,
					  parTwoLines, 
					  angleTwoLines, 
					  hor, 
					  ver)

mapped_operations = [
	('create_point', CreateManager.create_point),
	('create_line', CreateManager.create_line),

	('drag_point', None),
	('drag_line', None),

	('horizontal', RestrictionManager.horizontal_strict),
	('vertical', RestrictionManager.vertical_strict),
	('parallel', RestrictionManager.lines_parallel),
	('perpendicular', RestrictionManager.lines_perpendicular),

	('connect_points', RestrictionManager.connect_points), 

	('attach_point_to_line', RestrictionManager.attach_point_to_line),
	('angle_between_lines', ToolManager.angle_between_lines),
	
	('dist_between_points', distTwoPoint),

	('test', printer)
]
