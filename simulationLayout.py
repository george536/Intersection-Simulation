import random
from enum import Enum

class Destination(Enum):
    East=1,
    North=2,
    West=3,
    South=4

class Source(Enum):
    East=1,
    North=2,
    West=3,
    South=4

class VehcileType(Enum):
    Self_Driven=0,
    Human_Driven=1


maxNumber=5
class Car:
    def __init__(self,Type, source, destination, lane):
        self.Type=Type
        self.source=source
        self.destination=destination
        self.lane=lane

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def isSelfDriven(self):
        return self.Type
    def getSource(self):
        return self.source
    def getDestination(self):
        return self.getDestination
    def getLane(self):
        return self.lane


class Lanes:
    global maxNumber
    def __init__(self):
        #pos means positive lane, cars are entering the intersection 
        #and exiting the lane (this is the right side of the road)
        self.lanePos1=[]
        self.lanePos2=[]
        self.lanePos3=[]
        #neg means negative lane, cars are exiting the intersection 
        #and entering the lane (this is the left side of the road)
        self.laneneg1=[]
        self.laneneg2=[]
        self.laneneg3=[]

        self.lanesSet=[self.lanePos1,
                    self.laneneg2,
                    self.lanePos3,
                    self.laneneg1,
                    self.laneneg2,
                    self.laneneg3]

    def update(self):
        self.lanesSet=[self.lanePos1,
                    self.laneneg2,
                    self.lanePos3,
                    self.laneneg1,
                    self.laneneg2,
                    self.laneneg3]

    def addCar(self,vehicle):
        if(vehicle.getSource()==Source.East):
            pass
            #check for limit
        if(vehicle.getSource()==Source.North):
            pass
            #check for limit
        if(vehicle.getSource()==Source.West):
            pass
            #check for limit
        if(vehicle.getSource()==Source.South):
            pass
            #check for limit

    
class Intersection:
    def __init__(self):
        self.rightDirection=Lanes()
        self.leftDirection=Lanes()
        self.topDirection=Lanes()
        self.bottomDirection=Lanes()

        self.fourWay=[self.rightDirection,
                    self.leftDirection,
                    self.topDirection,
                    self.bottomDirection]

    def update(self):
        self.fourWay=[self.rightDirection,
                    self.leftDirection,
                    self.topDirection,
                    self.bottomDirection]

    def addToEast(self):
            pass
    def addToNorth(self):
        pass
    def addToWest(self):
        pass
    def addToSouth(self):
        pass

    def randomGenerater(self):
        #randomly select where the car is coming from
        origion=random.choice(list(Source))
        #randomly select where the car is going
        destination=random.choice(list(Destination))
        #randomly select type of car
        Type=random.choice(list(VehcileType))


        if(destination.value!=origion.value):
            if(origion==1):
                self.rightDirection.addCar(Car(Type,origion,destination,0))
            if(origion==2):
                self.topDirection.addCar(Car(Type,origion,destination,0))
            if(origion==3):
                self.leftDirection.addCar(Car(Type,origion,destination,0))
            if(origion==4):
                self.bottomDirection.addCar(Car(Type,origion,destination,0))

             #if origin%2 == destination%2 #going straight
            #positive 2 lane
            #goign neg 2 lane
        #else
            #if abs(origin-destination)==1
                #if origin > destination #turning right
                    #positive 1 lane
                    #going neg 1 lane
                #else #turning left
                    #if self driving
                        #positive 1 lane
                        #going neg 1 lane (more needs to be done here)
                    #else human
                        #positive 3 lane
                        #going into neg 3 lane
            #else
                #if origin > destination #turning left
                    #if self driving
                        #positive 1 lane
                        #going neg 1 lane (more needs to be done here)
                    #else human
                        #positive 3 lane
                        #going into neg 3 lane
                #else #turning right
                    #positive 1 lane
                    #going neg 1 lane


    #ignore the draw function for now
    def draw():
        width=36
        height=30
        #y for height
        #x for width
        #¦
        for y in range(0,height+1):
            for x in range(0,width):
                #upper vertical part
                if((y>=0 and y<(height/3)) and (x==width/3 or x==width*2/3)):
                    print("█",end="")
                #horizontal part
                elif((y==height/3 or y==height*2/3) and (x<width/3-1 or x>width*2/3)):
                    print("",end=" ")
                #lower vertical part
                elif(y>height*2/3 and y<=height) and (x==width/3 or x==width*2/3):
                    print("█",end="")
                #vertical island
                elif (x==width/2 and (1<y<(height/3) or height>y>height*2/3)):
                    print("▩",end="")
                #hroizontal island
                elif (y==height/2 and (1<x<(width/3) or x>(width*2/3))):
                    print("▩",end=" ")
                #first lane line from top left
                elif (y>=0 and y<(height/3) and (x==int((((width/2)-(width/3))*1/3)+width/3))):
                    print(" ¦ ",end="")
                #second lane line from top left
                elif (y>=0 and y<(height/3) and (x==int((((width/2)-(width/3))*2/3)+width/3))):
                    print(" ¦ ",end="")
                #third lane line from top left
                elif (y>=0 and y<(height/3) and (x==int((((width*2/3)-(width/2))*1/3)+width/2))):
                    print(" ¦ ",end="")
                #fourth lane line from top left
                elif (y>=0 and y<(height/3) and (x==int((((width*2/3)-(width/2))*2/3)+width/2))):
                    print(" ¦ ",end="")
                elif (y>height*2/3 and y<(height) and (x==int((((width/2)-(width/3))*1/3)+width/3))):
                    print(" ¦ ",end="")
                #second lane line from top left
                elif (y>height*2/3 and y<(height) and (x==int((((width/2)-(width/3))*2/3)+width/3))):
                    print(" ¦ ",end="")
                #third lane line from top left
                elif (y>height*2/3 and y<(height) and (x==int((((width*2/3)-(width/2))*1/3)+width/2))):
                    print(" ¦ ",end="")
                #fourth lane line from top left
                elif (y>height*2/3 and y<(height) and (x==int((((width*2/3)-(width/2))*2/3)+width/2))):
                    print(" ¦ ",end="")    
                #white space inside vertically
                elif ((x>=width/3 and x<=width*2/3) and (y<=height/3 or y>=height*2/3)):
                    print(" ",end="")
                elif ((x<=width/3 or x>=width*2/3) and (y>=height/3 and y<=height*2/3)):
                    print(" ",end="")
                #print the white space for outer intersection area
                else:
                    print(" ",end=" ")
            print("\n")

    def display(self):
        for i in range(0,4):
            for lanes in self.rightDirection:
                for lane in lanes:
                    for car in lane:
                        print("Is it self-driven: ",car.isSelfDriven(),"Source: ",car.getSource, "in lane number: ", car.getLane(), "destination: ",car.getDestination(),"\n")


def main():
    design = Intersection()
    i=0
    while(i<5):
        design.randomGenerater()
        i+=1
    design.display()

main()
