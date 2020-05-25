import math

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    #  print(f"Distance:{dist}")
     return dist  

class TrafficLight:
    def __init__(self, name, route, Position, traficlight = []):
        self.name = name
        self.route = route
        self.status = "Red"
        self.cars = []
        self.bikes = []
        self.pedestrians = []
        self.buses = []
        self.Position = Position
        self.nextTraficLight = traficlight

class Car():
    def __init__(self, TrafficLight):
        self.TrafficLight = TrafficLight
        TrafficLight.cars.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1
        self.isWaiting = False
        # print("New car!")

    def drive(self):
        MaxD = 30
        self.isWaiting = False

        for c in self.TrafficLight.cars:
            
            if c != self and self.TrafficLight.cars[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:  # tegen collision detectie in bochten
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y)
                if distance < MaxD:
                    self.isWaiting = True
                    break
        
        try:
            if self == self.TrafficLight.cars[1]:
                dist = calculateDistance(self.TrafficLight.cars[1].x,self.TrafficLight.cars[1].y, self.TrafficLight.cars[0].x,self.TrafficLight.cars[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:  # tegen collision detectie in bochten
                        self.isWaiting = False
        except IndexError:
            DontUseException = True
            
        if self.TrafficLight.cars[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
            distance = calculateDistance(self.x, self.y, self.TrafficLight.route[1][0],self.TrafficLight.route[1][1])

            if distance < 10:
                self.isWaiting = True

        if self.driveIndex >= 1 and self.TrafficLight.status == "Green":
            self.isWaiting = False
                
        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]:
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex:
            del self
            return
        if self.isWaiting == True:
             return

        if self.isWaiting == False:
            if self.y > self.TrafficLight.route[self.driveIndex][1]:
                self.y -= self.speed
            if self.y < self.TrafficLight.route[self.driveIndex][1]:
                self.y += self.speed
            if self.x > self.TrafficLight.route[self.driveIndex][0]:
                self.x -= self.speed
            if self.x < self.TrafficLight.route[self.driveIndex][0]:
                self.x += self.speed

    #def __del__(self):
        #print("car destroyed")

class Bike():
    def __init__(self, TrafficLight):
        self.TrafficLight = TrafficLight
        TrafficLight.bikes.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1

    def drive(self):
        MaxD = 30
        self.isWaiting = False

        for c in self.TrafficLight.bikes:
            
            if c != self and self.TrafficLight.bikes[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:  # tegen collision detectie in bochten
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y)
                if distance < MaxD:               
                    self.isWaiting = True        
                    break
        
        try:
            if self == self.TrafficLight.bikes[1]:
                dist = calculateDistance(self.TrafficLight.bikes[1].x,self.TrafficLight.bikes[1].y, self.TrafficLight.bikes[0].x,self.TrafficLight.bikes[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:  # tegen collision detectie in bochten
                        self.isWaiting = False
        except IndexError:
            DontUseException = True

        if self.TrafficLight.bikes[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
            distance = calculateDistance(self.x, self.y, self.TrafficLight.route[1][0],self.TrafficLight.route[1][1])

            if distance < 10:
                self.isWaiting = True

        if self.driveIndex >= 1 and self.TrafficLight.status == "Green":
            self.isWaiting = False                

        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]:
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex:
            self.TrafficLight.bikes.remove(self)
            self.TrafficLight.nextTraficLight.append(self)
            del self
            return
        if self.isWaiting == True:
             return

        if self.isWaiting == False:
            if self.y > self.TrafficLight.route[self.driveIndex][1]:
                self.y -= self.speed
            if self.y < self.TrafficLight.route[self.driveIndex][1]:
                self.y += self.speed
            if self.x > self.TrafficLight.route[self.driveIndex][0]:
                self.x -= self.speed
            if self.x < self.TrafficLight.route[self.driveIndex][0]:
                self.x += self.speed

class Pedestrian():
    def __init__(self, TrafficLight):
        self.TrafficLight = TrafficLight
        TrafficLight.pedestrians.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1

    def drive(self):
        MaxD = 30
        self.isWaiting = False

        for c in self.TrafficLight.pedestrians:
            
            if c != self and self.TrafficLight.pedestrians[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:  # tegen collision detectie in bochten
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y)
                if distance < MaxD:             
                    self.isWaiting = True        
                    break
        
        try:
            if self == self.TrafficLight.pedestrians[1]:
                dist = calculateDistance(self.TrafficLight.pedestrians[1].x,self.TrafficLight.pedestrians[1].y, self.TrafficLight.pedestrians[0].x,self.TrafficLight.pedestrians[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:  # tegen collision detectie in bochten
                        self.isWaiting = False
        except IndexError:
            DontUseException = True
            
        if self.TrafficLight.pedestrians[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
            distance = calculateDistance(self.x, self.y, self.TrafficLight.route[1][0],self.TrafficLight.route[1][1])

            if distance < 10:
                self.isWaiting = True

        if self.driveIndex >= 1 and self.TrafficLight.status == "Green":
            self.isWaiting = False
                
        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]:
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex:
            del self
            return
        if self.isWaiting == True:
             return

        if self.isWaiting == False:
            if self.y > self.TrafficLight.route[self.driveIndex][1]:
                self.y -= self.speed
            if self.y < self.TrafficLight.route[self.driveIndex][1]:
                self.y += self.speed
            if self.x > self.TrafficLight.route[self.driveIndex][0]:
                self.x -= self.speed
            if self.x < self.TrafficLight.route[self.driveIndex][0]:
                self.x += self.speed


class Bus():
    def __init__(self, TrafficLight):
        self.TrafficLight = TrafficLight
        TrafficLight.buses.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1

    def drive(self):
        MaxD = 30
        self.isWaiting = False

        for c in self.TrafficLight.buses:
            
            if c != self and self.TrafficLight.buses[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:  # tegen collision detectie in bochten
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y)
                if distance < MaxD:             
                    self.isWaiting = True        
                    break
        
        try:
            if self == self.TrafficLight.buses[1]:
                dist = calculateDistance(self.TrafficLight.buses[1].x,self.TrafficLight.buses[1].y, self.TrafficLight.buses[0].x,self.TrafficLight.buses[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:  # tegen collision detectie in bochten
                        self.isWaiting = False
        except IndexError:
            DontUseException = True
            
        if self.TrafficLight.buses[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
            distance = calculateDistance(self.x, self.y, self.TrafficLight.route[1][0],self.TrafficLight.route[1][1])

            if distance < 10:
                self.isWaiting = True

        if self.driveIndex >= 1 and self.TrafficLight.status == "Green":
            self.isWaiting = False
                
        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]:
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex:
            del self
            return
        if self.isWaiting == True:
             return

        if self.isWaiting == False:
            if self.y > self.TrafficLight.route[self.driveIndex][1]:
                self.y -= self.speed
            if self.y < self.TrafficLight.route[self.driveIndex][1]:
                self.y += self.speed
            if self.x > self.TrafficLight.route[self.driveIndex][0]:
                self.x -= self.speed
            if self.x < self.TrafficLight.route[self.driveIndex][0]:
                self.x += self.speed

class TrafficObject:
    def __init__(self, A1, A2, A3, A4, AB1, AB2, B1, B2, B3, B4, B5, BB1, C1, C2, C3, D1, D2, D3, E1, EV1, EV2, EV3, EV4, FF1, FF2, FV1, FV2, FV3, FV4, GF1, GF2, GV1, GV2, GV3, GV4):
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
