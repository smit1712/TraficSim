# region Imports
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
    NEXT_SPAWN_CAR, NEXT_SPAWN_BIKE, NEXT_SPAWN_PEDESTRIAN, NEXT_SPAWN_BUS, ALL_Vehicles
# endregion

# region Initialize variables
seed(1) # Randomization seed for spawning entities

SPAWN = True # Set to False to stop spawning

TYPES = ['car', 'bike', 'pedestrian', 'bus']

# Maps the images to the entities
ENTITY_TYPE = {
    'car': CAR_IMG,
    'bike': BIKE_IMG,
    'bus': BUS_IMG,
    'pedestrian': PEDESTRIAN_IMG[randint(0, len(PEDESTRIAN_IMG)-1)],
    'crossroad': CROSS_ROAD_IMG
}

# Basic configuration for entity spawning
ENTITY_SPAWN = {
    'car': [
        lambda: CARS.append(Car(LIGHTS[randint(0, len(LIGHTS) - 1)])), # Add new spawned cars to the trafficlight
        NEXT_SPAWN_CAR, # Start time to spawn
        timedelta(seconds=7) # Interval to spawn next
        ],
    'bike': [
        lambda: BIKES.append(Bike(LIGHTS_BIKE[randint(0, len(LIGHTS_BIKE) - 1)])),
        NEXT_SPAWN_BIKE,
        timedelta(seconds=25)
        ],
    'pedestrian': [
        lambda: PEDESTRIANS.append(Pedestrian(LIGHTS_PEDESTRIAN[randint(0, len(LIGHTS_PEDESTRIAN) - 1)])),
        NEXT_SPAWN_PEDESTRIAN,
        timedelta(seconds=25)
        ],
    'bus': [
        lambda: BUSES.append(Bus(LIGHTS_BUS[randint(0, len(LIGHTS_BUS) - 1)])),
        NEXT_SPAWN_BUS,
        timedelta(seconds=60)
        ]
}

# Maps light state to color
LIGHT_COLOR = {
    'Green': GREEN,
    'Orange': ORANGE,
    'Red': RED
}
# endregion

# region draw
def draw_light(light, color):
    pygame.draw.rect(GAME_DISPLAY, LIGHT_COLOR[color],
        (light.Position[0], light.Position[1], 25, 25), 0)

def draw_entity(x, y, type):
    GAME_DISPLAY.blit(ENTITY_TYPE[type], (x, y))
# endregion

# region spawn
# Create new entity for the given type
def spawn_entity(now, type):
    if SPAWN:
        if(now > ENTITY_SPAWN[type][1]):
            ENTITY_SPAWN[type][0]()
            ENTITY_SPAWN[type][1] = now + ENTITY_SPAWN[type][2]
# endregion

# region mainloop
async def main():
    global CRASHED
    global NEXT_SPAWN_CAR
    global SPAWN

    while not CRASHED:
        now = datetime.now()
        for event in pygame.event.get(): # Handle user input
            if event.type == pygame.QUIT:
                CRASHED = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())  # Get mouse pointer location
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
            if event.type == KEYDOWN and event.key == K_d:
                SPAWN = True

        draw_entity(0, 0, 'crossroad') # Draw map

        for l in ALL_LIGHTS: # Set light status
            if l.nextTraficLight != []:
                if l.nextTraficLight.status == "Green":
                    draw_light(l.nextTraficLight, l.nextTraficLight.status)
                if l.nextTraficLight.status == "Orange":
                    draw_light(l.nextTraficLight, l.nextTraficLight.status)
                if l.nextTraficLight.status == "Red":
                    draw_light(l.nextTraficLight, l.nextTraficLight.status)

            if l.status == "Green":
                draw_light(l, l.status)
            if l.status == "Orange":
                draw_light(l, l.status)
            if l.status == "Red":
                draw_light(l, l.status)

        for c in CARS: # Update car position
            if c.driveIndex == len(c.TrafficLight.route): # If destination reached
                CARS.remove(c)
                c.TrafficLight.vehicles.remove(c) # Remove from the list
                del c # Delete object
                break
            c.drive()
            draw_entity(c.x, c.y, 'car')

        if BIKES != None:
            for b in BIKES:
                if b.driveIndex == len(b.TrafficLight.route):
                    BIKES.remove(b)
                    try:
                        b.TrafficLight.vehicles.remove(b)
                    except ValueError:
                        Nothing = True # Everything is permitted
                    del b
                    break
                b.drive()
                draw_entity(b.x, b.y, 'bike')

        if PEDESTRIANS != None:
            for p in PEDESTRIANS:
                if p.driveIndex == len(p.TrafficLight.route):
                    PEDESTRIANS.remove(p)
                    try:
                        p.TrafficLight.vehicles.remove(p)
                    except ValueError:
                        Nothing = True
                    del p
                    break
                p.drive()
                draw_entity(p.x, p.y, 'pedestrian')

        if BUSES != None:
            for b in BUSES:
                if b.driveIndex == len(b.TrafficLight.route):
                    BUSES.remove(b)
                    b.TrafficLight.vehicles.remove(b)
                    del b
                    break
                b.drive()
                draw_entity(b.x, b.y, 'bus')

        for x in range(0, len(TYPES)): # Cycle through entities
            spawn_entity(now, TYPES[x-1])

        pygame.display.update() # Update screen
        CLOCK.tick(120)

    # Handles shutting down application
    ws_receive.raise_exception()
    ws_send.raise_exception()
    ws_receive.join()
    ws_send.join()
    sys.exit()
# endregion

# region initialize
if __name__ == "__main__":
    try:
        ws = create_connection(URI)
        ws_receive = ThreadingReceive('receive_1', ws)
        ws_send = ThreadingSend('send_2', ws)
        ws_receive.start()
        ws_send.start()
        asyncio.run(main())
    except WebSocketAddressException:
        print("No websocket connection, now trying without websocket.")
        asyncio.run(main())
    except ConnectionRefusedError:
        print("Connection refused, now trying without connection.")
        asyncio.run(main())
# endregion
