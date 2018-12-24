from lab2.nx_geometry.services.extractor import data_parser
from lab2.nx_geometry.operators.mapper import mapped_operations


@data_parser
def handle_data(data, operation):
	for rule in mapped_operations:
		if rule[0] == operation:
			return rule[1](data)
	raise ValueError('Operation {} is not defined'.format(operation))
