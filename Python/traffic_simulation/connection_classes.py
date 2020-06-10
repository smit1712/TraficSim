# region import
import threading
import asyncio
import json
import time
import ctypes

from traffic_simulation import URI, LIGHTS, LIGHTS_BIKE, LIGHTS_PEDESTRIAN, LIGHTS_BUS, ALL_LIGHTS
from traffic_simulation.objects import TrafficLight
# endregion

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
            for l in ALL_LIGHTS: # Map received light status to trafficlight color
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
        self.ws.close()

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
        while(True): # Gathers all trafficlights and their traffic
            data = {
                "A1": len(LIGHTS[0].vehicles), "A2": len(LIGHTS[1].vehicles), "A3": len(LIGHTS[2].vehicles), "A4": len(LIGHTS[3].vehicles), "AB1": len(LIGHTS_BUS[0].vehicles), "AB2": len(LIGHTS_BUS[1].vehicles),
                "B1": len(LIGHTS[4].vehicles), "B2": len(LIGHTS[5].vehicles), "B3": len(LIGHTS[6].vehicles), "B4": len(LIGHTS[7].vehicles), "B5": len(LIGHTS[8].vehicles), "BB1": len(LIGHTS_BUS[2].vehicles),
                "C1":  len(LIGHTS[9].vehicles), "C2": len(LIGHTS[10].vehicles), "C3": len(LIGHTS[11].vehicles), "D1": len(LIGHTS[12].vehicles), "D2": len(LIGHTS[13].vehicles), "D3": len(LIGHTS[14].vehicles),
                "E1": len(LIGHTS_BIKE[0].vehicles), "EV1": len(LIGHTS_PEDESTRIAN[0].vehicles), "EV2": len(LIGHTS_PEDESTRIAN[0].nextTraficLight.pedestrians), 
                "EV3": len(LIGHTS_PEDESTRIAN[1].nextTraficLight.pedestrians), "EV4": len(LIGHTS_PEDESTRIAN[1].vehicles),
                "FF1": len(LIGHTS_BIKE[1].vehicles), "FF2": len(LIGHTS_BIKE[2].vehicles), "FV1": len(LIGHTS_PEDESTRIAN[2].vehicles), "FV2":len(LIGHTS_PEDESTRIAN[2].nextTraficLight.pedestrians), "FV3":len(LIGHTS_PEDESTRIAN[3].nextTraficLight.pedestrians),
                "FV4": len(LIGHTS_PEDESTRIAN[3].vehicles), "GF1": len(LIGHTS_BIKE[3].vehicles), "GF2": len(LIGHTS_BIKE[4].vehicles),
                "GV1": len(LIGHTS_PEDESTRIAN[4].vehicles), "GV2": len(LIGHTS_PEDESTRIAN[4].nextTraficLight.pedestrians), "GV3": len(LIGHTS_PEDESTRIAN[5].nextTraficLight.pedestrians), "GV4":len(LIGHTS_PEDESTRIAN[5].vehicles)
                }
            json_dump = json.dumps(data)
            self.ws.send(json_dump)
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
