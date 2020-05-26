import threading
import asyncio
import json
import time
import ctypes
from traffic_simulation import URI, LIGHTS, LIGHTS_BIKE, LIGHTS_PEDESTRIAN, LIGHTS_BUS, ALL_LIGHTS
from traffic_simulation.objects import TrafficLight

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
            for l in ALL_LIGHTS:
                status = js[l.name] 
                if l.nextTraficLight != []:
                    if status == 2:
                        l.nextTraficLight.status = "Green"
                    elif status == 1:
                        l.nextTraficLight.status = "Orange"
                    else:
                        l.nextTraficLight.status = "Red"
                if status == 2:
                    l.status = "Green"
                elif status == 1:
                    l.status = "Orange"
                else:
                    l.status = "Red"
                #print(f"Received: {data}")
        self.ws.close()
        print("websocketclosed")
    
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


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
            data = {"A1": len(LIGHTS[0].cars), "A2": len(LIGHTS[1].cars), "A3": len(LIGHTS[2].cars), "A4": len(LIGHTS[3].cars), "AB1": len(LIGHTS_BUS[0].buses), "AB2": len(LIGHTS_BUS[1].buses),
                    "B1": len(LIGHTS[4].cars), "B2": len(LIGHTS[5].cars), "B3": len(LIGHTS[6].cars), "B4": len(LIGHTS[7].cars), "B5": len(LIGHTS[8].cars), "BB1": len(LIGHTS_BUS[2].buses),
                    "C1":  len(LIGHTS[9].cars), "C2": len(LIGHTS[10].cars), "C3": len(LIGHTS[11].cars), "D1": len(LIGHTS[12].cars), "D2": len(LIGHTS[13].cars), "D3": len(LIGHTS[14].cars),
                    "E1": len(LIGHTS_BIKE[0].bikes), "EV1": len(LIGHTS_PEDESTRIAN[0].pedestrians), "EV2": len(LIGHTS_PEDESTRIAN[0].nextTraficLight.pedestrians), 
                    "EV3": len(LIGHTS_PEDESTRIAN[1].nextTraficLight.pedestrians), "EV4": len(LIGHTS_PEDESTRIAN[1].pedestrians),
                    "FF1": len(LIGHTS_BIKE[1].bikes), "FF2": len(LIGHTS_BIKE[2].bikes), "FV1": len(LIGHTS_PEDESTRIAN[2].pedestrians), "FV2":len(LIGHTS_PEDESTRIAN[2].nextTraficLight.pedestrians), "FV3":len(LIGHTS_PEDESTRIAN[3].nextTraficLight.pedestrians),
                    "FV4": len(LIGHTS_PEDESTRIAN[3].pedestrians), "GF1": len(LIGHTS_BIKE[3].bikes), "GF2": len(LIGHTS_BIKE[4].bikes),
                    "GV1": len(LIGHTS_PEDESTRIAN[4].pedestrians), "GV2": len(LIGHTS_PEDESTRIAN[4].nextTraficLight.pedestrians), "GV3": len(LIGHTS_PEDESTRIAN[5].nextTraficLight.pedestrians), "GV4":len(LIGHTS_PEDESTRIAN[5].pedestrians)}
            json_dump = json.dumps(data)
            self.ws.send(json_dump)
            #print(f"Send: {json_dump}")
            time.sleep(1)

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
