import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8090/api/websocket"
    async with websockets.connect(uri) as websocket:
        # Subscribe to time updates
        subscribe_message = {
            "type": "time",
            "id": 1,
            "options": {
                "instance": "myproject"
            }
        }
        await websocket.send(json.dumps(subscribe_message))
        
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
