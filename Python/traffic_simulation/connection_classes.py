import threading
import asyncio
import json
import time

from traffic_simulation import URI, LIGHTS

class ThreadingReceive(threading.Thread):
    def __init__(self, thread_id, websocket):
        self.stop_thread = False
        self.ws = websocket
        self.thread_number = thread_id
        threading.Thread.__init__(self)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self.websocket_receive())
        asyncio.get_event_loop().run_forever()

    async def websocket_receive(self):
        print(f"WS CONNECTED ON: {URI} Thread id: {self.thread_number}")
        while(True):
            data = self.ws.recv()
            js = json.loads(data)
            for l in LIGHTS:
                status = js[l.name]
                if status == 2:
                    l.status = "Green"
                else:
                    l.status = "Red"
            print(f"Received: {data}")
        self.ws.close()
        print("websocketclosed")


class ThreadingSend(threading.Thread):
    def __init__(self, thread_id, websocket):
        self.stop_thread = False
        self.ws = websocket
        self.thread_number = thread_id
        threading.Thread.__init__(self)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(self.websocket_send())
        asyncio.get_event_loop().run_forever()

    async def websocket_send(self):
        while(True):
            data = {"A1": len(LIGHTS[0].cars), "A2": len(LIGHTS[1].cars), "A3": len(LIGHTS[2].cars), "A4": len(LIGHTS[3].cars), "AB1": 0, "AB2": 0,
                    "B1": len(LIGHTS[4].cars), "B2": len(LIGHTS[5].cars), "B3": len(LIGHTS[6].cars), "B4": 0, "B5": 0, "BB1": 0,
                    "C1":  len(LIGHTS[7].cars), "C2": len(LIGHTS[8].cars), "C3": len(LIGHTS[9].cars), "D1": len(LIGHTS[10].cars), "D2": len(LIGHTS[11].cars), "D3": len(LIGHTS[12].cars),
                    "E1": 0, "EV1": 0, "EV2": 0, "EV3": 0, "EV4": 0,
                    "FF1": 0, "FF2": 0, "FV1": 0, "FV2": 0, "FV3": 0, "FV4": 0,
                    "GF1": 0, "GF2": 0, "GV1": 0, "GV2": 0, "GV3": 0, "GV4": 0}
            json_dump = json.dumps(data)
            self.ws.send(json_dump)
            print(f"Send: {json_dump}")
            time.sleep(1)
