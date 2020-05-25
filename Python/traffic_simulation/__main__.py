import asyncio, sys, os
import pygame, pyautogui, math
import threading
import json
from datetime import datetime, timedelta
from random import seed, randint
from websocket import create_connection, WebSocketAddressException
from pygame.locals import *

from traffic_simulation.connection_classes import ThreadingReceive, ThreadingSend
from traffic_simulation.objects import TrafficLight, Car, Bike, Pedestrian, Bus
from traffic_simulation import URI, CRASHED, GAME_DISPLAY, GREEN, ORANGE, RED, CLOCK, CROSS_ROAD_IMG, CAR_IMG, \
    BIKE_IMG, BUS_IMG, PEDESTRIAN_IMG,ALL_LIGHTS, LIGHTS, LIGHTS_BIKE, LIGHTS_PEDESTRIAN, LIGHTS_BUS, CARS, BIKES, PEDESTRIANS, BUSES, \
    NEXT_SPAWN_CAR, NEXT_SPAWN_BIKE, NEXT_SPAWN_PEDESTRIAN, NEXT_SPAWN_BUS, NEXT_GREEN, NEXT_SEND, ALL_Vehicles

seed(1)

SPAWN = True

TYPES = ['car', 'bike', 'pedestrian', 'bus']

ENTITY_TYPE = {
    'car': CAR_IMG,
    'bike': BIKE_IMG,
    'bus': BUS_IMG,
    'pedestrian': PEDESTRIAN_IMG[randint(0, len(PEDESTRIAN_IMG)-1)],
    'crossroad': CROSS_ROAD_IMG
}

ENTITY_SPAWN = {
    'car': [
        lambda: CARS.append(Car(LIGHTS[randint(0, len(LIGHTS) - 1)])),
        NEXT_SPAWN_CAR,
        timedelta(seconds=1),
        CARS
        ],
    'bike': [
        lambda: BIKES.append(Bike(LIGHTS_BIKE[randint(0, len(LIGHTS_BIKE) - 1)])),
        NEXT_SPAWN_BIKE,
        timedelta(seconds=10),
        BIKES
        ],
    'pedestrian': [
        lambda: PEDESTRIANS.append(Pedestrian(LIGHTS_PEDESTRIAN[randint(0, len(LIGHTS_PEDESTRIAN) - 1)])),
        NEXT_SPAWN_PEDESTRIAN,
        timedelta(seconds=30),
        PEDESTRIANS
        ],
    'bus': [
        lambda: BUSES.append(Bus(LIGHTS_BUS[randint(0, len(LIGHTS_BUS) - 1)])),
        NEXT_SPAWN_BUS,
        timedelta(seconds=40),
        BUSES
        ]
}

def draw_entity(x, y, type):
    GAME_DISPLAY.blit(ENTITY_TYPE[type], (x, y))

def spawn_entity(now, type):
    if SPAWN:
        if(now > ENTITY_SPAWN[type][1]):
            ENTITY_SPAWN[type][0]()
            ENTITY_SPAWN[type][1] = now + ENTITY_SPAWN[type][2]

async def main():
    global CRASHED
    global NEXT_SPAWN_CAR
    global SPAWN

    while not CRASHED:
        now = datetime.now()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                CRASHED = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                ws_receive.raise_exception()
                ws_send.raise_exception()
                ws_receive.join()
                ws_send.join()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_c:
                os.system('cls')
            if event.type == KEYDOWN and event.key == K_s:
                SPAWN = False            

        draw_entity(0, 0, 'crossroad')
        x, y = pygame.mouse.get_pos()

        for c in CARS:
            # print(f"Drive index: {c.driveIndex} Trafficlight route: {len(c.TrafficLight.route)}")
            if c.driveIndex == len(c.TrafficLight.route):
                CARS.remove(c)
                c.TrafficLight.cars.remove(c)
                del c
                break
            c.drive()
            draw_entity(c.x, c.y, 'car')

        if BIKES != None:
            for b in BIKES:
                # print(f"Drive index: {c.driveIndex} Trafficlight route: {len(c.TrafficLight.route)}")
                if b.driveIndex == len(b.TrafficLight.route):
                    BIKES.remove(b)
                    try:
                        b.TrafficLight.bikes.remove(b)
                    except ValueError:
                        Nothing = True
                    del b
                    break
                b.drive()
                draw_entity(b.x, b.y, 'bike')

        if PEDESTRIANS != None:
            for p in PEDESTRIANS:
                # print(f"Drive index: {c.driveIndex} Trafficlight route: {len(c.TrafficLight.route)}")
                if p.driveIndex == len(p.TrafficLight.route):
                    PEDESTRIANS.remove(p)
                    p.TrafficLight.pedestrians.remove(p)
                    del p
                    break
                p.drive()
                draw_entity(p.x, p.y, 'pedestrian')

        if BUSES != None:
            for b in BUSES:
                # print(f"Drive index: {c.driveIndex} Trafficlight route: {len(c.TrafficLight.route)}")
                if b.driveIndex == len(b.TrafficLight.route):
                    BUSES.remove(b)
                    b.TrafficLight.buses.remove(b)
                    del b
                    break
                b.drive()
                draw_entity(b.x, b.y, 'bus')

        for x in range(0, 4):
            spawn_entity(now, TYPES[x])

        # if(now > nextGreen):
        #     i = randint(0, len(lights) -1)
        #     for l in lights:
        #         l.status = "Red"
        #     lights[i].status = "Green"
        #     print(lights[i].name)
        #     nextGreen = now + timedelta(seconds=10)
        # if(now > nextSend):
            # asyncio.get_event_loop().run_until_complete(websocket_send())
            # nextSpawn = datetime.now() + timedelta(seconds=5)

        for l in ALL_LIGHTS:
            if l.status == "Green":
                pygame.draw.rect(GAME_DISPLAY, GREEN,
                                 (l.Position[0], l.Position[1], 25, 25), 0)
            if l.status == "Orange":
                pygame.draw.rect(GAME_DISPLAY, ORANGE,
                                 (l.Position[0], l.Position[1], 25, 25), 0)
            if l.status == "Red":
                pygame.draw.rect(GAME_DISPLAY, RED,
                                 (l.Position[0], l.Position[1], 25, 25), 0)

        pygame.display.update()
        CLOCK.tick(120)

    ws_receive.raise_exception()
    ws_send.raise_exception()
    ws_receive.join()
    ws_send.join()
    sys.exit()

if __name__ == "__main__":
    try:
        ws = create_connection(URI)
        ws_receive = ThreadingReceive('receive_1', ws)
        ws_send = ThreadingSend('send_2', ws)
        ws_receive.start()
        ws_send.start()
        asyncio.run(main())
    except WebSocketAddressException:
        print("This program has crashed, not trying without websocket")
        asyncio.run(main())
