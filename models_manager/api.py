import asyncio
import websockets

class ManagerAPI:

    async def hello(self, websocket):
        name = await websocket.recv()
        print(f"<<< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f">>> {greeting}")

    async def main(self):
        async with websockets.serve(self.hello, "0.0.0.0", 5000):
            await asyncio.Future()  # run forever

if __name__ == "__main__":

    server = ManagerAPI()
    asyncio.run(server.main())
