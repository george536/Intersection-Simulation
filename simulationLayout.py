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

class LaneType(Enum):
    rightMost=1,
    middle=2,
    leftMost=3,

class Traffic(Enum):
    EastWest=1,
    NorthSouth=2,
    NorthSouthLeftTurn=3,
    EastWestLeftTurn=4

currentTrafic=Traffic.EastWest
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
        
    
class Intersection:
    def __init__(self):
        self.East=Lanes()
        self.West=Lanes()
        self.North=Lanes()
        self.South=Lanes()
        self.currentTrafic=currentTrafic

        self.fourWay=[self.East,
                    self.West,
                    self.North,
                    self.South]

    def update(self):
        self.fourWay=[self.East,
                    self.West,
                    self.North,
                    self.South]

        self.currentTrafic=currentTrafic

    def controlTraffic(self):
        global currentTrafic
        #put code here
        self.currentTrafic=currentTrafic
        pass

    def canTakeMore(self,lane):
        if(len(lane)<=maxNumber):
            return True
        else:
            return False

    def addToEast(self,Type,origion,destination):
        #car turning right or self-driven car turning right to go left
        if(destination==Destination.North or (destination==Destination.South and Type==VehcileType.Self_Driven)):
            if(self.canTakeMore(self.East.lanePos1)):
                self.East.lanePos1.append(Car(Type,origion,destination,LaneType.rightMost))

        #Human-driven car turning left
        elif(destination==Destination.South and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.East.lanePos2)):
                self.East.lanePos2.append(Car(Type,origion,destination,LaneType.middle))

        #self-driven car going straight
        elif(destination==Destination.West and Type==VehcileType.Self_Driven):
            if(self.canTakeMore(self.East.lanePos1)):
                self.East.lanePos1.append(Car(Type,origion,destination,LaneType.rightMost))
            elif(self.canTakeMore(self.East.lanePos3)):
                self.East.lanePos3.append(Car(Type,origion,destination,LaneType.leftMost))

        #human-driev car going straight
        elif(destination==Destination.West and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.East.lanePos1)):
                self.East.lanePos1.append(Car(Type,origion,destination,LaneType.rightMost))


    def addToNorth(self,Type,origion,destination):
        pass
    def addToWest(self,Type,origion,destination):
        pass
    def addToSouth(self,Type,origion,destination):
        pass

    def randomCarGenerater(self):
        origion=random.choice(list(Source))
        destination=random.choice(list(Destination))
        Type=random.choice(list(VehcileType))


        if(destination.value!=origion.value):
            if(origion==Source.East):
                self.addToEast(Type,origion,destination)
            if(origion==Source.North):
                self.addToNorth(Type,origion,destination)
            if(origion==Source.West):
                self.addToWest(Type,origion,destination)
            if(origion==Source.South):
                self.addToSouth(Type,origion,destination)

    def SarahsComments():

        ################### Sarah's Comments ######################            

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

        pass
    ############# ignore the draw function for now ###################
    def draw():
        width=36
        height=30
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
        for laneSet in self.fourWay:
            for lanes in laneSet.lanesSet:
                for lane in lanes:
                    for car in lane:
                        print("Is it self-driven: ",car.isSelfDriven(),"Source: ",car.getSource(), "in lane number: ", car.getLane(), "destination: ",car.getDestination(),"\n")


def main():
    sim = Intersection()
    i=0
    while(i<5):
        sim.randomCarGenerater()
        i+=1
    sim.display()

main()
