from enum import Enum
from msilib.schema import Extension
import os
import random
import time
from tkinter import E

class Directions(Enum):
    East=1
    North=2
    West=3
    South=4

class VehcileType(Enum):
    Self_Driven=0
    Human_Driven=1


class Traffic(Enum):
    EastWest=1
    NorthSouth=2
    NorthSouthLeftTurn=3
    EastWestLeftTurn=4

class Destination(Enum):
    right=1
    straight=2
    left=3

class EastCoord:
    x=[15,17,19,21,23]
    y=[7,9,11]

class WestCoord:
    x=[8,6,4,2,0]
    y=[17,15,13]

# class EastLaneSorting(Enum):
#     Right:2
#     Straight:3
#     Left:4


# class NorthLaneSorting(Enum):
#     Right:3
#     Straight:4
#     Left:1

# class WestLaneSorting(Enum):
#     Right:4
#     Straight:1
#     Left:2
    

# class SouthLaneSorting(Enum):
#     Right:1
#     Straight:2
#     Left:3

class Lane:
    def __init__(self,size):
        self.size=size
        self.Array=[0 for i in range(size)]
        self.count=0

    def increaseCount(self):
        self.count+=1

    def decreaseCount(self):
        self.count-=1

    def getCount(self):
        return self.count
    
    def getArray(self):
        return self.Array

maxNumber=5

class Car:
    def __init__(self,type, destination, x, y):
        self.type=type
        self.destination=destination
        self.x=x
        self.y=y

    def getType(self):
        return self.type
    def getDestination(self):
        return self.destination
    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Lanes:
    global maxNumber
    def __init__(self):
        self.lanePos1=Lane(maxNumber)
        self.lanePos2=Lane(maxNumber)
        self.lanePos3=Lane(maxNumber)
        self.laneNeg1=Lane(maxNumber)
        self.laneNeg2=Lane(maxNumber)
        self.laneNeg3=Lane(maxNumber)

        self.lanesSet=[self.lanePos1,
                    self.lanePos2,
                    self.lanePos3,
                    self.laneNeg1,
                    self.laneNeg2,
                    self.laneNeg3]

    def update(self):
        self.lanesSet=[self.lanePos1,
                    self.lanePos2,
                    self.lanePos3,
                    self.laneNeg1,
                    self.laneNeg2,
                    self.laneNeg3]

class Intersection:
    def __init__(self):
        self.East=Lanes()
        self.West=Lanes()
        self.North=Lanes()
        self.South=Lanes()
        self.currentTrafic=Traffic.EastWest
        self.fourWay=[self.East,
                    self.West,
                    self.North,
                    self.South]

    def update(self):
        self.East.update()
        self.North.update()
        self.West.update()
        self.South.update()

        self.fourWay=[self.East,
                    self.West,
                    self.North,
                    self.South]

    def addToLanes(self,type,turn,lane,directionEnum):
        global maxNumber
        if(turn==Destination.right and lane.lanePos1.getCount()<maxNumber):
            count=lane.lanePos1.getCount()
            lane.lanePos1.getArray()[count]=Car(type,turn,directionEnum.x[count],directionEnum.y[0])
            lane.lanePos1.increaseCount()

        elif(turn==Destination.straight):
            count=lane.lanePos1.getCount()
            if(count<maxNumber):
                lane.lanePos1.getArray()[count]=Car(type,turn,directionEnum.x[count],directionEnum.y[0])
                lane.lanePos1.increaseCount()

            elif (count==maxNumber and type==VehcileType.Self_Driven and lane.lanePos3.getCount()<maxNumber):
                count=lane.lanePos3.getCount()       
                lane.lanePos3.getArray()[count]=Car(type,turn,directionEnum.x[count],directionEnum.y[2])
                lane.lanePos3.increaseCount()

        elif(turn==Destination.left and lane.lanePos2.getCount()<maxNumber):
            count=lane.lanePos2.getCount()
            lane.lanePos2.getArray()[count]=Car(type,turn,directionEnum.x[count],directionEnum.y[1])
            lane.lanePos2.increaseCount()

    def randomCarGenerater(self):
        origion=random.choice(list(Directions))
        turn=random.choice(list(Destination))
        type=random.choice(list(VehcileType))

        if(origion==Directions.East):
            self.addToLanes(type,turn,self.East,EastCoord)
        if(origion==Directions.North):
            self.addToLanes(type,turn,self.North,EastCoord)
        if(origion==Directions.West):
            self.addToLanes(type,turn,self.West,WestCoord)
        if(origion==Directions.South):
            self.addToLanes(type,turn,self.South,EastCoord)

    def isIn(self,x,y):
        for lane in self.fourWay:
            for innerLane in lane.lanesSet:
                for car in innerLane.getArray():
                    if(car!=0):
                        if(car.getX()==x and car.getY()==y):
                            return True
                        
        return False

    def draw(self):
        os.system('cls')
        width=24
        height=24
        #y for height
        #x for width
        #¦
        for y in range(0,height+1):
            for x in range(0,width+1):
                #upper vertical part
                if((6>y>=0 or y>18) and (x==5 or x==17)):
                    print("█",end="")
                elif((6>y>0 or 24>y>18) and (x==11)):
                    print("|",end="")
                elif((6>y>=0 or y>18) and (x==7 or x==9 or x==13 or x==15)):
                    print("¦",end="")
                elif((6>y>=0 or y>18) and x<6):
                    print(" ",end="  ")
                elif ((y==6 or y==18) and (x<6 or 18>x>11)):
                    print("=",end="  ")
                elif (y==12 and (1<x<7 or 20>x>14)):
                    print("-",end=" ")
                elif ((x<7 or 22>x>14) and (y==8 or y==10 or y==14 or y==16)):
                    print("--",end="")
                
                elif self.isIn(x,y):
                    print("C",end="")
                elif(y>5 and y<19):
                    print(" ",end=" ")
                else:
                    print(" ",end="") 
            print("")


def main():

    sim = Intersection()
    sim.currentTrafic=Traffic.EastWest
    
    #global timer
    timer=0
    while(True):    
        sim.draw()
        sim.randomCarGenerater()
        print(sim.currentTrafic)
        # sim.move()
        # sim.controlTraffic()
        # randomDelete=random.randint(0,2)
        # if randomDelete==0:
        #     sim.carsLeaving()
        time.sleep(0.1)
        #timer+=0.5
    

main()
