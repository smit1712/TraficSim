import logging
import os, sys
import pygame
from datetime import datetime, timedelta

from traffic_simulation.objects import TrafficLight, Car, Bike, Pedestrian, Bus

# region Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
# endregion

# region Connection settings
URI = "ws://trafic.azurewebsites.net/controller"
# endregion

# region Global vars
CRASHED = False
GREEN = (0, 255, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)

LIGHTS = [
    TrafficLight("A1", [(637, 885), (633, 596), (608, 452), 
                        (546, 411), (467, 398), (399, 400),
                        (289, 402), (209, 402), (120, 395), 
                        (9, 404)], (633, 596)),
    TrafficLight("A2", [(672, 891), (659, 596), (649, 9)], (659, 596)),
    TrafficLight("A3", [(699, 891), (689, 596), (683, 13)], (689, 596)),
    TrafficLight("A4", [(720, 889), (715, 596), (738, 529), (831, 495), (940, 488), (1067, 485), (1217, 475)], (715, 596)),
    TrafficLight("B1", [(587, 9), (591, 305), (603, 403), (646, 455), (697, 478), (752, 488), (886, 479), (992, 480), (1096, 476), (1167, 473), (1225, 471)], (591, 305)),
    TrafficLight("B2", [(555, 14), (562, 310), (572, 891)], (562, 310)),
    TrafficLight("B3", [(517, 19), (527, 314), (539, 891)], (527, 314)),
    TrafficLight("B4", [(495, 20), (501, 304), (472, 355), (416, 383), (296, 394), (10, 407)], (501, 304)),
    TrafficLight("C1", [(1224, 445), (788, 428), (605, 460), (561, 536), (567, 890)], (788, 428)),
    TrafficLight("C2", [(1230, 410), (788, 398), (6, 407)], (788, 398)),
    TrafficLight("C3", [(1236, 376), (795, 361), (692, 320), (681, 11)], (795, 361)),
    TrafficLight("D1", [(6, 478), (334, 470), (622, 461), (687, 402), (677, 8)], (334, 470)),
    TrafficLight("D2", [(10, 502), (339, 495), (1222, 475)], (339, 495)),
    TrafficLight("D3", [(4, 524), (329, 524), (523, 518), (563, 550), (571, 890)], (329, 524))
]

LIGHTS_BIKE = [
    TrafficLight('E1', [(1135, 240), (727, 237), (437, 239), (411, 194), (408, 9)], (727, 237)),
    TrafficLight('FF1', [(374, 887), (387, 554),
                         (388, 430), (382, 307), (391, 13)], (387, 554)),
    TrafficLight('FF2', [(407, 10), (412, 330), (416, 571), (401, 714), (399, 785), (400, 880)], (412, 330)),
    TrafficLight('GF1', [(994, 656), (782, 659),
                         (449, 657), (366, 575), (7, 576)], (782, 659)),
    TrafficLight('GF2', [(393, 892), (455, 659), (784, 657), (1180, 643), (1234, 642)], (455, 659))
]

LIGHTS_PEDESTRIAN = [
    TrafficLight('EV1', [(1111, 203), (728, 211), (629, 212), (448, 217), (408, 211), (406, 11)], (728, 211)),
    TrafficLight('EV4', [(391, 7), (432, 227), (605, 224), (791, 215), (990, 215), (1111, 209), (1212, 203), (1229, 211)], (432, 227)),
    TrafficLight('FV1', [(1111, 203), (728, 211), (629, 212), (448, 217), (408, 211), (406, 11)], (728, 211)),
    TrafficLight('FV4', [(390, 10), (386, 328), (387, 435), (379, 553), (355, 613), (259, 604), (146, 604), (8, 608)], (386, 328)),
    TrafficLight('GV1', [(1149, 671), (784, 679), (617, 670), (459, 671), (373, 671), (371, 851), (369, 886)],  (784, 679)),
    TrafficLight('GV2', [(366, 693), (456, 684), (597, 693), (771, 689), (1025, 673), (1228, 676)], (456, 684))
]

LIGHTS_BUS = [
    TrafficLight('BB1', [(460, 24), (467, 297), (469, 346), (434, 374), (403, 390), (332, 395), (265, 395), (198, 399), (103, 398), (14, 405)], (467, 297)),
    TrafficLight('AB1', [(745, 891), (745, 740), (737, 656), (733, 575), (769, 533), (834, 494), (903, 483), (965, 483), (1058, 486), (1126, 483), (1207, 475), (1236, 475)] , (745, 740))
]

ALL_LIGHTS = [*LIGHTS, *LIGHTS_BIKE, *LIGHTS_PEDESTRIAN, *LIGHTS_BUS]

CARS = [Car(LIGHTS[0])]
BIKES = []
PEDESTRIANS = []
BUSES = []

NEXT_SPAWN_CAR = datetime.now() + timedelta(seconds=1)
NEXT_SPAWN_BIKE= datetime.now() + timedelta(seconds=10)
NEXT_SPAWN_PEDESTRIAN = datetime.now() + timedelta(seconds=30)
NEXT_SPAWN_BUS = datetime.now() + timedelta(seconds=40)
NEXT_GREEN = datetime.now() + timedelta(0, 3)
NEXT_SEND = datetime.now() + timedelta(0, 3)
# endregion

# region Pygame settings
pygame.init()
pygame.display.set_mode

display_width = 1238
display_height = 897

GAME_DISPLAY = pygame.display.set_mode(
    (display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption('traffic simulator')

CLOCK = pygame.time.Clock()

CROSS_ROAD_IMG = pygame.image.load('verkeerslichten.png')
CAR_IMG = pygame.image.load("car.jpg").convert_alpha()
BIKE_IMG = pygame.image.load('bike.jpg').convert_alpha()
PEDESTRIAN_IMG = [pygame.image.load('pedestrian_coffee.jpg').convert_alpha(),
                  pygame.image.load('pedestrian_dog.jpg').convert_alpha(),
                  pygame.image.load('pedestrian_female.jpg').convert_alpha()]
BUS_IMG = pygame.image.load('bus.jpg').convert_alpha()
# endregion
