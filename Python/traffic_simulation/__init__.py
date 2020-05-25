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
URI = "ws://45dfac58.ngrok.io"
# endregion

# region Global vars
CRASHED = False
GREEN = (0, 255, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)

LIGHTS = [
    TrafficLight("A1", [(624, 895), (619, 712), (621, 600), (608, 430), (350, 385), (7, 391)],(621, 600)),
    TrafficLight("A2", [(656, 894), (651, 715), (652, 601), (645, 4)],  (652, 601)),
    TrafficLight("A3", [(680, 892), (680, 712), (682, 597), (673, 7)], (682, 597)),
    TrafficLight("A4", [(714, 893), (710, 800), (713, 598), (717, 545), (731, 524), (755, 501), (781, 485), (1228, 463)],(713, 598)),
    TrafficLight("B1", [(573, 3), (575, 174), (578, 310), (578, 398), (597, 427), (634, 465), (697, 483), (761, 480), (1215, 468)], (578, 310)),
    TrafficLight("B2", [(546, 3), (548, 177), (551, 313), (559, 891)],(551, 313)),
    TrafficLight("B3", [(515, 5), (516, 160), (525, 312), (528, 895)], (525, 312)),
    TrafficLight("B4", [(485, 4), (488, 157), (488, 310), (455, 344), (422, 365), (352, 382), (3, 394)], (488, 310)),
    TrafficLight("B5", [(440, 1), (389, 222), (279, 341), (229, 385), (13, 398)], (279, 341)),

    TrafficLight("C1", [(1235, 373), (872, 411), (786, 418), (584, 439), (550, 487), (557, 856), (558, 889)], (786, 418)),
    TrafficLight("C2", [(1233, 375), (869, 382), (784, 381), (5, 391)],  (784, 381)),
    TrafficLight("C3", [(1227, 376), (871, 355), (787, 350), (719, 324), (677, 268), (672, 5)],  (787, 350)),
    TrafficLight("D1", [(1, 460), (256, 458), (427, 457), (608, 419), (669, 305), (669, 10)], (427, 457)),
    TrafficLight("D2", [(0, 491), (255, 486), (430, 483), (1230, 463)],(430, 483)),
    TrafficLight("D3", [(2, 521), (255, 515), (429, 511), (551, 544), (554, 718), (557, 884)], (429, 511))
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
    TrafficLight('EV1', [(623, 201), (623, 201), (448, 217), (408, 211), (406, 11)], (432, 180)),
    TrafficLight('EV2', [(1111, 203), (726, 204), (623, 201)], (623, 201)),
    TrafficLight('EV3', [(391, 7), (432, 227), (435, 213), (619, 210)], (435, 213)),
    TrafficLight('EV4', [(619, 210), (726, 214), (791, 215), (990, 215), (1111, 209), (1212, 203), (1229, 211)], (726, 204)),
    TrafficLight('FV1', [(1111, 203), (728, 211), (629, 212), (448, 217), (408, 211), (406, 11)], (728, 211)),
    TrafficLight('FV4', [(390, 10), (386, 328), (387, 435), (379, 553), (355, 613), (259, 604), (146, 604), (8, 608)], (386, 328)),
    TrafficLight('GV1', [(1149, 671), (784, 679), (617, 670), (459, 671), (373, 671), (371, 851), (369, 886)],  (784, 679)),
    TrafficLight('GV2', [(366, 693), (456, 684), (597, 693), (771, 689), (1025, 673), (1228, 676)], (456, 684))
]

LIGHTS_BUS = [
    TrafficLight('AB1', [(735, 893), (737, 803), (680, 597), (670, 5)], (764, 740)),
    TrafficLight('AB2', [(738, 804), (716, 597), (727, 532), (776, 500), (839, 478), (1228, 462)] , (764, 741)),
    TrafficLight('BB1', [(452, 2), (453, 174), (454, 314), (486, 644), (483, 891)], (454, 314))
]

ALL_LIGHTS = [*LIGHTS, *LIGHTS_BIKE, *LIGHTS_PEDESTRIAN, *LIGHTS_BUS]

CARS = [Car(LIGHTS[0])]
BIKES = []
PEDESTRIANS = []
BUSES = []

ALL_Vehicles = [*CARS, *BIKES, *PEDESTRIANS, *BUSES]

NEXT_SPAWN_CAR = datetime.now() + timedelta(seconds=10)
NEXT_SPAWN_BIKE= datetime.now() + timedelta(seconds=15)
NEXT_SPAWN_PEDESTRIAN = datetime.now() + timedelta(seconds=15)
NEXT_SPAWN_BUS = datetime.now() + timedelta(seconds=30)
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
