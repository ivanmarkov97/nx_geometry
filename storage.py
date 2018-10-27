from services.coders import json_encode, json_decode
import redis
import json


"""
change to dict
"""

class Storage:
	redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

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
	def set_restrictions(cls, d):
		cls.redis_db.set("restrictions", json.dumps(d))

	@classmethod
	def get_restiction_for_object(cls, uid):
		restictions = cls.redis_db.get("restictions")
		if restictions is not None:
			print("restictions NOT NONE")
			restictions = json.loads(restictions)
			if uid in restictions.keys():
				print("if")
				return restictions[uid]
			print("ELSE")
			return {}
		print("REDIS NOEN")
		return None

	@classmethod
	def get_all_restrictions(cls):
		restictions = cls.redis_db.get("restictions")
		if restictions is not None:
			return json.loads(restictions)
		return None

	@classmethod
	def export_all_data(cls):
		data_str = str([{key: cls.redis_db.get(key)} for key in cls.redis_db.keys() if key != "restrictions"])
		data_str = data_str.replace("b'", '"').replace("'", '"')
		data_str = data_str.replace('"{', '{').replace('}"', '}')
		return data_str
