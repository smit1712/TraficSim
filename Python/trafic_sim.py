import pygame, pyautogui, math
from datetime import datetime, timedelta
from random import seed
from random import randint
import asyncio
import websockets
import json

    


class traffic_object:
    def __init__(self, A1, A2, A3, A4, AB1, AB2, B1, B2, B3, B4, B5, BB1, C1, C2, C3, D1, D2, D3, E1, E2, EV1, EV2, EV3, EV4, FF1, FF2, FV1, FV2, FV3, FV4, GF1, GF2, GV1, GV2, GV3, GV4):
        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.A4 = A4
        self.AB1 = AB1
        self.AB2 = AB2
        self.B1 = B1
        self.B2 = B2
        self.B3 = B3
        self.B4 = B4
        self.B5 = B5
        self.BB1 = BB1
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3
        self.D1 = D1
        self.D2 = D2
        self.D3 = D3
        self.E1 = E1
        self.E2 = E2
        self.EV1 = EV1
        self.EV2 = EV2
        self.EV3 = EV3
        self.EV4 = EV4
        self.FF1 = FF1
        self.FF2 = FF2
        self.FV1 = FV1
        self.FV2 = FV2
        self.FV3 = FV3
        self.FV4 = FV4
        self.GF1 = GF1
        self.GF2 = GF2
        self.GV1 = GV1
        self.GV2 = GV2
        self.GV3 = GV3
        self.GV4 = GV4

async def websocket_init():
    uri = "ws://trafic.azurewebsites.net/controller"
    ws = await websockets.connect(uri)
    return ws

async def websocket_receive(websockets):
    while(not crashed):
        data = await ws.recv()
        print(f"< {data}")
    websockets.close()
    

async def websocket_send():
    data = {"A1": len(lights[0].cars), "A2": len(lights[1].cars), "A3": len(lights[2].cars), "A4": len(lights[3].cars), "AB1": 0, "AB2": 0,
                "B1": len(lights[4].cars), "B2": len(lights[5].cars), "B3": len(lights[6].cars), "B4": 0, "B5":0, "BB1": 0,
                "C1":  len(lights[7].cars), "C2": len(lights[8].cars), "C3": len(lights[9].cars), "D1": len(lights[10].cars), "D2": len(lights[11].cars), "D3": len(lights[12].cars),
                "E1": 0, "E2": 0, "EV1": 0, "EV2": 0, "EV3": 0, "EV4": 0,
                "FF1": 0, "FF2": 0, "FV1": 0, "FV2": 0, "FV3": 0, "FV4": 0,
                "GF1": 0, "GF2": 0, "GV1": 0, "GV2": 0, "GV3": 0, "GV4": 0}
    uri1 = "ws://trafic.azurewebsites.net/controller"
    # json_dump = json.dumps(data)
    # await main.ws.send(json_dump)  
    # greeting = await main.ws.recv()

    # print(f"< {greeting}")


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
    if(datetime.now() > nextSend):
        asyncio.get_event_loop().run_until_complete(websocket_send())     
        nextSpawn = datetime.now() + timedelta(0,2)


    for l in lights:
        if l.status == "Green":
            pygame.draw.rect(gameDisplay, GREEN, (l.Position[0],l.Position[1],25,25), 0)     
        if l.status == "Red":
            pygame.draw.rect(gameDisplay, RED, (l.Position[0],l.Position[1],25,25), 0)     


    pygame.display.update()
    clock.tick(120)

pygame.quit()
quit()

# def main():
#     ws = websocket_init()
#     asyncio.get_event_loop().run_forever(websocket_receive(ws))    

# if __name__ == '__main__':
#     main()