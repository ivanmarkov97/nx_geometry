from operators.handler import handle_data
from storage import Storage
import websockets
import asyncio

async def hello(websocket, path):
	await websocket.send(Storage.export_all_data())
	while True:
		try:
			data = await websocket.recv()
			data = handle_data(data)
			await websocket.send(Storage.export_all_data())
		except websockets.exceptions.ConnectionClosed:
			break

Storage.redis_db.flushall()
start_server = websockets.serve(hello, 'localhost', 65432)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
