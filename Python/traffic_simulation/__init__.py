import logging
import os, sys
import pygame
from datetime import datetime, timedelta

from traffic_simulation.objects import TrafficLight, Car

# region Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
# endregion

# region Connection settings
URI = "ws://61c85c95.ngrok.io/"
# endregion

# region Global vars
CRASHED = False
GREEN = (0, 255, 0)
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
                        (548, 609), (572, 713), (572, 886)], (272, 528)),
]

CARS = [Car(LIGHTS[0])]

NEXT_SPAWN = datetime.now() + timedelta(0, 1)
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
pygame.display.set_caption('trafic sim')

CLOCK = pygame.time.Clock()

CROSS_ROAD_IMG = pygame.image.load('verkeerslichten.png')
CAR_IMG = pygame.image.load("car.jpg").convert_alpha()
# endregion
