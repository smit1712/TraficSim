import math

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
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
        try:
            if self.TrafficLight.bikes[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
                distance = calculateDistance(self.x, self.y, self.TrafficLight.route[1][0],self.TrafficLight.route[1][1])

                if distance < 10:
                    self.isWaiting = True
        except IndexError:
            DontUseException = True
        if self.driveIndex >= 1 and self.TrafficLight.status == "Green":
            self.isWaiting = False

        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]:
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex:
            if self.TrafficLight.nextTraficLight != []:
                self.TrafficLight.bikes.remove(self)
                self.TrafficLight.nextTraficLight.bikes.append(self)
                self.TrafficLight = self.TrafficLight.nextTraficLight
                self.driveIndex = 0
            else:
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
        try:
            if self.TrafficLight.pedestrians[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
                distance = calculateDistance(self.x, self.y, self.TrafficLight.route[1][0],self.TrafficLight.route[1][1])

                if distance < 10:
                    self.isWaiting = True
        except IndexError:
            DontUseException = True

        if self.driveIndex >= 1 and self.TrafficLight.status == "Green":
            self.isWaiting = False

        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]:
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex:
            if self.TrafficLight.nextTraficLight != []:
                self.TrafficLight.pedestrians.remove(self)
                self.TrafficLight.nextTraficLight.pedestrians.append(self)
                self.TrafficLight = self.TrafficLight.nextTraficLight

                self.driveIndex = 0
            else:
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
