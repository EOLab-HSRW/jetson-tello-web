import asyncio
import websockets
import json
import time



async def process(websocket,path):

	while not websocket.closed:
		count = 0
		async for message in websocket:

            #Assigning response
			# response = {"name":"ilgar","surname":"rasulov"}
			# response = json.dumps(response)
			response = "Hello, "+message+" !"
            
			await websocket.send(response)

async def main ():
	async with websockets.serve(process, "0.0.0.0", 4040, ping_interval = None):
		await asyncio.Future()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

