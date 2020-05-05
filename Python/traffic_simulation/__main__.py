import pygame
import pyautogui
import math
import asyncio
from datetime import datetime, timedelta
from random import seed
from random import randint
import websockets
import threading

from traffic_simulation.connection_classes import ThreadingReceive, ThreadingSend
from traffic_simulation.objects import TrafficLight, Car
from traffic_simulation import URI, CRASHED, GAME_DISPLAY, GREEN, RED, CLOCK, CROSS_ROAD_IMG, CAR_IMG, LIGHTS, CARS, \
    NEXT_SPAWN, NEXT_GREEN, NEXT_SEND

seed(1)

def threading_temp():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(connect_server())
    loop.run_forever()

async def connect_server():
    websocket = websockets.connect(URI)
    ws_receive = ThreadingReceive(1, websocket)
    ws_send = ThreadingSend(2, websocket)
    ws_receive.start()
    ws_send.start()
    return

def cross_road(x, y):
    GAME_DISPLAY.blit(CROSS_ROAD_IMG, (x, y))

def draw_car(x, y):
    GAME_DISPLAY.blit(CAR_IMG, (x, y))

def main():
    global CRASHED
    global NEXT_SPAWN

    t = threading.Thread(target=threading_temp)
    t.start()

    while not CRASHED:
        now = datetime.now()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                CRASHED = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        cross_road(0, 0)

        x, y = pygame.mouse.get_pos()
        for c in CARS:
            if c.driveIndex == len(c.TrafficLight.route):
                CARS.remove(c)
                c.TrafficLight.cars.remove(c)
                del c
                break
            c.drive()
            draw_car(c.x, c.y)

        if(now > NEXT_SPAWN):
            i = randint(0, len(LIGHTS) - 1)
            CARS.append(Car(LIGHTS[i]))
            NEXT_SPAWN = now + timedelta(seconds=3)

        # if(now > nextGreen):
        #     i = randint(0, len(lights) -1)
        #     for l in lights:
        #         l.status = "Red"
        #     lights[i].status = "Green"
        #     print(lights[i].name)
        #     nextGreen = now + timedelta(seconds=10)
        # # if(now > nextSend):
        #     # asyncio.get_event_loop().run_until_complete(websocket_send())
        #     # nextSpawn = datetime.now() + timedelta(seconds=5)

        for l in LIGHTS:
            if l.status == "Green":
                pygame.draw.rect(GAME_DISPLAY, GREEN,
                                 (l.Position[0], l.Position[1], 25, 25), 0)
            if l.status == "Red":
                pygame.draw.rect(GAME_DISPLAY, RED,
                                 (l.Position[0], l.Position[1], 25, 25), 0)

        pygame.display.update()
        CLOCK.tick(120)
    ThreadingReceive.stop_threads = True
    ThreadingSend.stop_threads = True
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()