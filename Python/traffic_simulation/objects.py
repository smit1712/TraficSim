import math

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

class TrafficLight:
    def __init__(self, name, route, Position, traficlight = []):
        self.name = name
        self.route = route
        self.status = "Red"
        self.vehicles = []
        self.Position = Position
        self.nextTraficLight = traficlight

class Car():
    def __init__(self, TrafficLight):
        self.TrafficLight = TrafficLight
        TrafficLight.vehicles.append(self) # Adds this vehicle to correct trafficlight
        self.y = TrafficLight.route[0][1] # Set spawn location from trafficlight to self
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0 # Set route node to 0
        self.speed = 1 # Amount of coordinates moved per update
        self.isWaiting = False # Entity is waiting until green trafficlight

    def drive(self):
        MaxD = 30 # Set collision range
        self.isWaiting = False

        for c in self.TrafficLight.vehicles: # Collision detection
            if c != self and self.TrafficLight.vehicles[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:  # Collision detection in turns
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y) # Measure distance till other entity
                if distance < MaxD:
                    self.isWaiting = True
                    break

        try:
            if self == self.TrafficLight.vehicles[1]: # Second car drives when trafficlight is green
                dist = calculateDistance(self.TrafficLight.vehicles[1].x,self.TrafficLight.vehicles[1].y, self.TrafficLight.vehicles[0].x,self.TrafficLight.vehicles[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:  # Collision detection in turns
                        self.isWaiting = False
        except IndexError:
            DontUseException = True

        if self.TrafficLight.vehicles[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green": # First car stops for red light
            distance = calculateDistance(self.x, self.y, self.TrafficLight.route[1][0],self.TrafficLight.route[1][1])

            if distance < 10:
                self.isWaiting = True

        if self.driveIndex >= 1 and self.TrafficLight.status == "Green": # If trafficlight is green, drive
            self.isWaiting = False

        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]: # Go to next route node
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex: # If at end destination, delete entity
            del self
            return
        if self.isWaiting == True:
             return

        if self.isWaiting == False: # Move from node to node
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
        TrafficLight.vehicles.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1

    def drive(self):
        MaxD = 30
        self.isWaiting = False

        for c in self.TrafficLight.vehicles:
            if c != self and self.TrafficLight.vehicles[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y)
                if distance < MaxD:
                    self.isWaiting = True
                    break

        try:
            if self == self.TrafficLight.vehicles[1]:
                dist = calculateDistance(self.TrafficLight.vehicles[1].x,self.TrafficLight.vehicles[1].y, self.TrafficLight.vehicles[0].x,self.TrafficLight.vehicles[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:
                        self.isWaiting = False
        except IndexError:
            DontUseException = True
        try:
            if self.TrafficLight.vehicles[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
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
            if self.TrafficLight.nextTraficLight != []: # Link next trafficlight
                self.TrafficLight.vehicles.remove(self)
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
        TrafficLight.vehicles.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1

    def drive(self):
        MaxD = 30
        self.isWaiting = False

        for c in self.TrafficLight.vehicles:

            if c != self and self.TrafficLight.vehicles[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y)
                if distance < MaxD:
                    self.isWaiting = True
                    break

        try:
            if self == self.TrafficLight.vehicles[1]:
                dist = calculateDistance(self.TrafficLight.vehicles[1].x,self.TrafficLight.vehicles[1].y, self.TrafficLight.vehicles[0].x,self.TrafficLight.vehicles[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:
                        self.isWaiting = False
        except IndexError:
            DontUseException = True
        try:
            if self.TrafficLight.vehicles[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
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
                self.TrafficLight.vehicles.remove(self)
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
        TrafficLight.vehicles.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1

    def drive(self):
        MaxD = 30
        self.isWaiting = False

        for c in self.TrafficLight.vehicles:
            if c != self and self.TrafficLight.vehicles[0] != c and c != self.isWaiting:
                if c.driveIndex > 1:
                    continue
                distance = calculateDistance(self.x, self.y, c.x,c.y)
                if distance < MaxD:
                    self.isWaiting = True
                    break

        try:
            if self == self.TrafficLight.vehicles[1]:
                dist = calculateDistance(self.TrafficLight.vehicles[1].x,self.TrafficLight.vehicles[1].y, self.TrafficLight.vehicles[0].x,self.TrafficLight.vehicles[0].y)
                if dist < MaxD:
                    self.isWaiting = True
                    if c.driveIndex > 2:
                        self.isWaiting = False
        except IndexError:
            DontUseException = True

        if self.TrafficLight.vehicles[0] == self and self.driveIndex == 1 and self.TrafficLight.status != "Green":
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
