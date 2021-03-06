# region import
import logging
import os, sys
import pygame
from datetime import datetime, timedelta

from traffic_simulation.objects import TrafficLight, Car, Bike, Pedestrian, Bus
# endregion

# region Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
# endregion

# region Connection uri
URI = "ws://localhost:5000" # Change this URL to connect to a different host
# endregion

# region Global vars
CRASHED = False
GREEN = (0, 255, 0)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)

# Configures all lights, roads and next lights
LIGHTS = [
    TrafficLight("A1", [(624, 895), (619, 712), (621, 600), (608, 430), (350, 385), (7, 391)],(621, 600)),
    TrafficLight("A2", [(656, 894), (651, 715), (652, 601), (645, 4)],  (652, 601)),
    TrafficLight("A3", [(680, 892), (680, 712), (682, 597), (673, 7)], (682, 597)),
    TrafficLight("A4", [(714, 893), (710, 800), (713, 598), (717, 545), (731, 524), (755, 501), (781, 485), (1228, 463)],(713, 598)),
    TrafficLight("B1", [(573, 3), (575, 174), (578, 310), (578, 398), (597, 427), (634, 465), (697, 483), (761, 480), (1215, 468)], (578, 310)),
    TrafficLight("B2", [(546, 3), (548, 177), (551, 313), (559, 891)],(551, 313)),
    TrafficLight("B3", [(515, 5), (516, 160), (525, 312), (528, 895)], (525, 312)),
    TrafficLight("B4", [(485, 4), (488, 157), (488, 310), (455, 344), (422, 365), (352, 382), (3, 394)], (488, 310)),
    TrafficLight("B5", [(391, 2), (305, 331), (279, 341), (229, 385), (13, 398)], (279, 341)),

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
                         (388, 430), (382, 307), (391, 13)], (398, 539)),
    TrafficLight('FF2', [(407, 10), (412, 330), (416, 571), (401, 714), (399, 785), (400, 880)], (400, 372)),
    TrafficLight('GF1', [(1230, 642), (772, 645), (613, 647), (385, 651), (390, 888)], (613, 647)),
    TrafficLight('GF2', [(369, 892), (463, 648), (566, 647), (1229, 645)],(566, 647))
]

LIGHTS_PEDESTRIAN = [
    TrafficLight('EV1', [(410, 4), (442, 215), (617, 210)],  (617, 210),
        TrafficLight('EV2', [(617, 210),(702, 208),(1231, 210)], (702, 208))),
    TrafficLight('EV4', [(1223, 209), (702, 206), (641, 208)], (641, 208),
        TrafficLight('EV3', [(641, 208), (450, 213), (402, 211), (401, 8)],(402, 211))),
    TrafficLight('FV1', [(388, 894), (373, 558), (373, 448)], (373, 448),
        TrafficLight('FV2', [(373, 448),(376, 419), (374, 369), (387, 1)], (374, 369))),

    TrafficLight('FV4', [(383, 4), (373, 321), (375, 417)], (375, 417),
        TrafficLight('FV3', [(375, 417),(374, 451), (373, 537), (347, 575), (5, 579)], (373, 537))),
    TrafficLight('GV1', [(1228, 673), (774, 675), (613, 675)], (613, 675),
        TrafficLight('GV2', [(613, 675), (486, 679), (422, 682), (359, 680), (350, 610), (6, 610)], (485, 688))),
    TrafficLight('GV4', [(376, 892), (442, 676), (562, 678)], (562, 678),
        TrafficLight('GV3', [ (562, 678), (611, 678), (753, 678), (1224, 680)], (753, 678)))
]

LIGHTS_BUS = [
    TrafficLight('AB1', [(735, 893), (737, 803), (680, 597), (670, 5)], (764, 714)),
    TrafficLight('AB2', [(738, 804), (716, 597), (727, 532), (776, 500), (839, 478), (1228, 462)] , (764, 741)),
    TrafficLight('BB1', [(452, 2), (453, 174), (454, 314), (486, 644), (483, 891)], (454, 314))
]

ALL_LIGHTS = [*LIGHTS, *LIGHTS_BIKE, *LIGHTS_PEDESTRIAN, *LIGHTS_BUS]

CARS = [Car(LIGHTS[0])]
BIKES = []
PEDESTRIANS = []
BUSES = []

ALL_Vehicles = [*CARS, *BIKES, *PEDESTRIANS, *BUSES]

# Initial spawn time
NEXT_SPAWN_CAR = datetime.now() + timedelta(seconds=10)
NEXT_SPAWN_BIKE= datetime.now() + timedelta(seconds=15)
NEXT_SPAWN_PEDESTRIAN = datetime.now() + timedelta(seconds=15)
NEXT_SPAWN_BUS = datetime.now() + timedelta(seconds=50)
# endregion

# region Pygame settings
pygame.init()

display_width = 1238
display_height = 897

GAME_DISPLAY = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption('Traffic Simulator')

CLOCK = pygame.time.Clock()

# Loading images
CROSS_ROAD_IMG = pygame.image.load('img/verkeerslichten.png')
CAR_IMG = pygame.image.load('img/car.jpg').convert_alpha()
BIKE_IMG = pygame.image.load('img/bike.jpg').convert_alpha()
PEDESTRIAN_IMG = [pygame.image.load('img/pedestrian_coffee.jpg').convert_alpha(),
                  pygame.image.load('img/pedestrian_dog.jpg').convert_alpha(),
                  pygame.image.load('img/pedestrian_female.jpg').convert_alpha()]
BUS_IMG = pygame.image.load('img/bus.jpg').convert_alpha()
# endregion
