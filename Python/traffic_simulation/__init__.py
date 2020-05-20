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
    TrafficLight("A1", [(631, 885), (629, 728), (634, 473),
                        (604, 399), (382, 386), (188, 394), (7, 398)], (629, 728)),
    TrafficLight("A2", [(664, 888), (660, 727), (656, 601),
                        (654, 240), (653, 8)], (660, 727)),
    TrafficLight("A3", [(696, 893), (688, 725),
                        (682, 242), (683, 5)], (688, 725)),
    TrafficLight("A4", [(721, 889), (713, 728), (726, 541),
                        (880, 486), (1197, 478)], (713, 728)),
    TrafficLight("B1", [(582, 10), (588, 253), (634, 417),
                        (714, 487), (942, 490), (1205, 472)], (588, 253)),
    TrafficLight("B2", [(554, 13), (553, 198), (556, 404),
                        (570, 686), (567, 887)], (553, 198)),
    TrafficLight("B3", [(527, 11), (533, 195), (539, 894)], (533, 195)),
    TrafficLight("B4", [(491, 10), (495, 180), (498, 309),
                        (463, 354), (391, 383), (175, 395), (7, 397)], (495, 180)),
    TrafficLight("C1", [(1223, 411), (890, 422), (736, 429),
                        (601, 472), (563, 585), (568, 875)], (890, 422)),
    TrafficLight("C2", [(1227, 385), (886, 391), (608, 400),
                        (291, 393), (7, 401)], (886, 391)),
    TrafficLight("C3", [(1224, 383), (885, 361), (715, 343),
                        (678, 226), (680, 18)], (885, 361)),
    TrafficLight("D1", [(9, 472), (270, 469), (609, 462),
                        (679, 313), (684, 19)], (270, 469)),
    TrafficLight("D2", [(19, 497), (263, 502), (597, 490),
                        (916, 484), (1195, 469)], (263, 502)),
    TrafficLight("D3", [(27, 532), (272, 528), (520, 523),
                        (548, 609), (572, 713), (572, 886)], (272, 528))
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
    TrafficLight('BB1', [(27, 532), (272, 528), (520, 523),
                         (548, 609), (572, 713), (572, 886)], (272, 528))
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
