from operators.handler import handle_data
import websockets
import asyncio

"""
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
"""

async def hello(websocket, path):
	while True:
	    data = await websocket.recv()
	    data = handle_data(data)
	    await websocket.send(data)

start_server = websockets.serve(hello, 'localhost', 65432)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
