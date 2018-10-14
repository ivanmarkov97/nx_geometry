import socket

host = '127.0.0.1'
port = 65432

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
while True:
	data = str(input('Input data: '))
	socket.send(data.encode())
	data = socket.recv(1024)
	if not data:
		break
	print(data)
