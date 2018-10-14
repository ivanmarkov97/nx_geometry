def point_encoder(point):
	json_point = {}
	json_point['object'] = point.__class__.__name__
	json_point['data'] = point.__dict__
	return json_point

def line_encoder(line):
	json_line = {}
	json_line['object'] = line.__class__.__name__
	json_line['data'] = []
	for p in line.points:
		json_line['data'].append(point_encoder(p))
	return json_line

encoder_map = {
	'Point': point_encoder,
	'Line': line_encoder
}

def json_encode(object_inst):
	return encoder_map[object_ins.__class__.__name__](object_inst)
