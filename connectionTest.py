from utils import *
import asyncio
import websockets
import json

url = 'ws://10.0.0.85:5000'

async def main():
    async with websockets.connect(url) as ws:
        message = json.dumps({
            'mode': 'rainbow',
            'data': [[(0, 0, 255), (0, 0, 0), (0, 0, 255)],
                     [(0, 0, 0), (255, 50, 0), (0, 0, 0)],
                     [(0, 0, 255), (0, 0, 0), (0, 0, 255)]]
        })

        await ws.send(message)

asyncio.run(main())