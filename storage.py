from services.coders import json_encode, json_decode
import redis
import json


"""
change to dict
"""

class Storage:
	def __init__(self, host="localhost", port=6379, db=0):
		self.redis_db = redis.StrictRedis(host=host, port=port, db=db)

	def add(self, obj):
		enc_obj = json_encode(obj)
		self.redis_db.set(obj.uid, enc_obj)

	def remove(self, obj):
		pass

	def remove_by_uid(self, obj):
		pass

	def get_by_uid(self, uid) -> str:
		data = self.export_json(uid)
		return json_decode(data)

	def export_json(self, uid) -> str:
		data = self.redis_db.get(uid)
		data = data.decode('utf8').replace("'", '"')
		return json.loads(data)

storage = Storage()
