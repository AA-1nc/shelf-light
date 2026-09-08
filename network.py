from utils import *
from websocket import create_connection
import json

class client:
    def __init__(self):
        # Replace 'address' with your device's ip address
        self.url = 'ws://address'
        self.ws = None

    def connect(self):
        self.ws = create_connection(self.url)

    def disconnect(self):
        if (self.ws):
            self.ws.close()
    
    def sendData(self, mode, data):
        print(f'{mode}\n{data}')
        if self.ws:
            self.ws.send(json.dumps({
                'mode': mode,
                'data': data
            }))