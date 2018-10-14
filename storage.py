from collections import OrderedDict
from services.encoders import json_encode
import json

class Storage:
	def __init__(self):
		self.objects = OrderedDict()

	def add(self, obj):
		self.objects[obj.uid] = obj

	def remove(self, obj):
		if obj.uid in self.objects:
			del self.objects[obj.uid]

	def export_json(self):
		export_data = []
		for obj in self.objects.items():
			export_data.append(json_encode(obj[1]))
		return json.dumps(export_data)

	@property
	def size(self):
		return len(self.objects)
