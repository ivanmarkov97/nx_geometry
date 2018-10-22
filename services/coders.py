from entities.primitives import Point, Line

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

def point_decoder(point_str):
	point_data = point_str['data']
	return Point((point_data['x'], point_data['y']), point_data['_uid'])

def line_decoder(line_str):
	points = []
	for point in line_str['data']:
		points.append(point_decoder(point))
	return Line(points[0], points[1], None)

encoder_map = {
	'Point': point_encoder,
	'Line': line_encoder
}

decoder_map = {
	'Point': point_decoder,
	'Line': line_decoder
}

def json_encode(object_inst):
	return encoder_map[object_inst.__class__.__name__](object_inst)

def json_decode(object_str):
	return decoder_map[object_str['object']](object_str)
