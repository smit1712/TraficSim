class TrafficLight:
    def __init__(self, name, route, Position):
        self.name = name
        self.route = route
        self.status = "Red"
        self.cars = []
        self.Position = Position

class Car:
    def __init__(self, TrafficLight):
        self.TrafficLight = TrafficLight
        TrafficLight.cars.append(self)
        self.y = TrafficLight.route[0][1]
        self.x = TrafficLight.route[0][0]
        self.driveIndex = 0
        self.speed = 1
        print("New car!")

    def drive(self):
        MaxD = 30

        for c in self.TrafficLight.cars:
            if c != self:
                if self.x in range(c.x - MaxD, c.x + MaxD) and self.y in range(c.y - MaxD, c.y + MaxD):
                    return
        if self.driveIndex == 1 and self.TrafficLight.status != "Green":
            if self.y == self.TrafficLight.route[1][1] and self.x == self.TrafficLight.route[1][0]:
                return

        if len(self.TrafficLight.route) == self.driveIndex:
            del self
            return

        if self.y == self.TrafficLight.route[self.driveIndex][1] and self.x == self.TrafficLight.route[self.driveIndex][0]:
            self.driveIndex = self.driveIndex + 1

        if len(self.TrafficLight.route) == self.driveIndex:
            del self
            return

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
