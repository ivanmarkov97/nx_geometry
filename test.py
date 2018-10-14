from entities.primitives import Point, Line
from storage import Storage
from services.encoders import json_encode
import json

p1 = Point((0.0, 0.0))
p2 = Point((1.0, 1.0))
l = Line(p1, p2)
print(l.length)
p1.x = 10.0
print(l.length)

s = Storage()
s.add(p1)
s.add(p2)
s.add(l)
print(s.export_json())
