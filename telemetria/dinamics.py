from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from random import randint
from asyncio import sleep

class GraphDinamics(WebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(1000):
            graph_values = {'engine_velocity':randint(-20, 20),
                            'car_velocity':randint(-20, 20),
                            'voltage':randint(-20, 20),
                            'current':randint(-20, 20),
                            'imu':randint(-20, 20),
                            'pwm':randint(-20, 20)}
            
            self.send(json.dumps(graph_values))
            sleep(1)



