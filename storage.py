from services.coders import json_encode, json_decode
import redis
import json


"""
change to dict
"""

class Storage:
	redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

	@classmethod
	def add(cls, obj):
		enc_obj = json_encode(obj)
		cls.redis_db.set(obj.uid, enc_obj)

	@classmethod
	def remove(cls, obj):
		pass

	@classmethod
	def remove_by_uid(cls, obj):
		pass

	@classmethod
	def get_by_uid(cls, uid) -> str:
		data = cls.export_json(uid)
		return json_decode(data)

	@classmethod
	def export_json(cls, uid) -> str:
		data = cls.redis_db.get(uid)
		data = data.decode('utf8').replace("'", '"')
		return json.loads(data)

	@classmethod
	def export_all_data(cls):
		return str([{key: cls.redis_db.hgetall(key)} for key in cls.redis_db.keys()])
