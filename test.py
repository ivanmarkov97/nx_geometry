from entities.primitives import Point, Line
from storage import storage
from services.coders import json_encode
import json

p1 = Point((0.0, 0.0))
p2 = Point((1.0, 1.0))
l = Line(p1, p2)
print(l.length)

storage.add(l)
#print(storage.get_by_uid(p1.uid), type(storage.get_by_uid(p1.uid)))
print(storage.get_by_uid(l.uid), type(storage.get_by_uid(l.uid)))
print(storage.redis_db.keys())
print(storage.redis_db.flushall())
