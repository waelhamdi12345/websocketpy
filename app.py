import asyncio
import websockets
import inspect

def my_function(arg1, arg2):
    pass

# Get the function signature
signature = inspect.signature(my_function)
print(signature.parameters)
connected_clients = {}

class MyWebSocket:
    async def __call__(self, websocket, path):
        connected_clients[id(websocket)] = websocket
        print(f"New connection! ({id(websocket)})")
        await websocket.send("Welcome to the Server.")
        try:
            async for message in websocket:
                await self.send_to_all(message)
        finally:
            del connected_clients[id(websocket)]

    async def send_to_all(self, message):
        for client in connected_clients.values():
            await client.send(message)

start_server = websockets.serve(MyWebSocket(), "0.0.0.0", 5000)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
