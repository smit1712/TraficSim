import pygame, pyautogui, math
from datetime import datetime, timedelta
from random import seed
from random import randint
import asyncio
import websockets
import json   


seed(1)
speed = 1
pygame.init()
pygame.display.set_mode

display_width = 1238
display_height = 897
GREEN = (0,255,0)
RED = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
pygame.display.set_caption('trafic sim')


clock = pygame.time.Clock()
crashed = False

crossRoadImg = pygame.image.load('verkeerslichten.png')
def crossroad(x, y):
    gameDisplay.blit(crossRoadImg, (x, y))

class traficlight:
    def __init__(self, name, route, Position):
        self.name = name
        self.route = route
        self.status = "Red"
        self.cars = [] 
        self.Position = Position

carImg = pygame.image.load("car.jpg").convert_alpha()

class car:
    def __init__(self, traficlight):
        self.traficlight = traficlight
        traficlight.cars.append(self)
        self.y = traficlight.route[0][1]
        self.x = traficlight.route[0][0]
        self.driveIndex = 0
    def drive(self):
        MaxD = 30

        for c in self.traficlight.cars:
            if c != self:
                if self.x in range(c.x - MaxD, c.x + MaxD) and self.y in range(c.y - MaxD, c.y + MaxD):
                    return
        if self.driveIndex == 1 and self.traficlight.status != "Green":
            if self.y == self.traficlight.route[1][1] and self.x == self.traficlight.route[1][0]:
                    return
                    
        if len(self.traficlight.route) == self.driveIndex:
                del self
                return

        if self.y == self.traficlight.route[self.driveIndex][1] and self.x == self.traficlight.route[self.driveIndex][0]:     
            self.driveIndex  =  self.driveIndex + 1

        if len(self.traficlight.route) == self.driveIndex:
                del self
                return
      
        if self.y > self.traficlight.route[self.driveIndex][1]:
            self.y -= speed
        if self.y < self.traficlight.route[self.driveIndex][1]:
            self.y += speed
        if self.x > self.traficlight.route[self.driveIndex][0]:
            self.x -= speed
        if self.x < self.traficlight.route[self.driveIndex][0]:
            self.x += speed

    #def __del__(self):
        #print("car destroyed")



def Drawcar(x, y):
    gameDisplay.blit(carImg, (x, y))


lights = [
    traficlight("A1", [(631, 885),(629, 728),(634, 473),(604, 399),(382, 386),(188, 394),(7, 398)],(629, 728) ),
    traficlight("A2", [(664, 888),(660, 727),(656, 601),(654, 240),(653, 8)] ,(660, 727) ),
    traficlight("A3", [(696, 893),(688, 725),(682, 242),(683, 5)], (688, 725)),
    traficlight("A4", [(721, 889),(713, 728),(726, 541),(880, 486),(1197, 478)],(713, 728)),
    traficlight("B1", [(582, 10),(588, 253),(634, 417),(714, 487),(942, 490),(1205, 472)],(588, 253)),
    traficlight("B2", [(554, 13),(553, 198),(556, 404),(570, 686),(567, 887)],(553, 198)),
    traficlight("B3", [(527, 11),(533, 195),(539, 894)],(533, 195)),
    traficlight("B4", [(491, 10),(495, 180),(498, 309),(463, 354),(391, 383),(175, 395),(7, 397)],(495, 180)),
    traficlight("C1", [(1223, 411),(890, 422),(736, 429),(601, 472),(563, 585),(568, 875)],(890, 422)),
    traficlight("C2", [(1227, 385),(886, 391),(608, 400),(291, 393),(7, 401)],(886, 391)),
    traficlight("C3", [(1224, 383),(885, 361),(715, 343),(678, 226),(680, 18)],(885, 361)),
    traficlight("D1", [(9, 472),(270, 469),(609, 462),(679, 313),(684, 19)],(270, 469)),
    traficlight("D2", [(19, 497),(263, 502),(597, 490),(916, 484),(1195, 469)],(263, 502)),
    traficlight("D3", [(27, 532),(272, 528),(520, 523),(548, 609),(572, 713),(572, 886)],(272, 528)),


 ]
cars = [car(lights[0])]

nextSpawn = datetime.now() + timedelta(0,1) 
nextGreen = datetime.now() + timedelta(0,3) 
nextSend = datetime.now() + timedelta(0,3) 


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

    crossroad(0, 0)

    x, y = pygame.mouse.get_pos()
    for c in cars:
        if c.driveIndex == len(c.traficlight.route):
           cars.remove(c)
           c.traficlight.cars.remove(c)
           del c
           break
        c.drive()   
        Drawcar(c.x, c.y)
 
    if(datetime.now() > nextSpawn):
        i = randint(0, len(lights) -1)
        cars.append(car(lights[i]))
        nextSpawn = datetime.now() + timedelta(0,2)

    if(datetime.now() > nextGreen):
        i = randint(0, len(lights) -1)
        for l in lights:
            l.status = "Red"
        lights[i].status = "Green"
        print(lights[i].name)
        nextGreen = datetime.now() + timedelta(0,15)
        
    # if(datetime.now() > nextSend):
    #     asyncio.get_event_loop().run_until_complete(websocket_send())     
    #     nextSpawn = datetime.now() + timedelta(0,2)


    for l in lights:
        if l.status == "Green":
            pygame.draw.rect(gameDisplay, GREEN, (l.Position[0],l.Position[1],25,25), 0)     
        if l.status == "Red":
            pygame.draw.rect(gameDisplay, RED, (l.Position[0],l.Position[1],25,25), 0)     


    pygame.display.update()
    clock.tick(120)

pygame.quit()
quit()
