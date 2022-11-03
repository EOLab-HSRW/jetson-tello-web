import asyncio
import websockets

HOST: str = "0.0.0.0"
PORT: int = 4040

async def launch():
    uri = f"ws://{HOST}:{PORT}"
    async with websockets.connect(uri) as websockets:
        await websockets.send("launch a model please")

        response = await websockets.recv()
        print(f"response from server: {response}")
    
async def hello():
    uri = f"ws://{HOST}:{PORT}"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())
