from operators.handler import handle_data
import socket

if __name__ == '__main__':
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.bind(('127.0.0.1', 65432))
	socket.listen(1)
	connection, address = socket.accept()
	while True:
		data = connection.recv(1024)
		if not data:
			break
		data = handle_data(data)
		connection.send(data)
