from services.extractor import data_parser
from operators.mapper import mapped_operations

@data_parser
def handle_data(data, operation):
	for rule in mapped_operations:
		if rule[0] == operation:
			return rule[1](data)
	raise ValueError('Operation {} is not defined'.format(operation))
