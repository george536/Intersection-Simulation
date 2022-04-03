from enum import Enum
import os
import random
import time


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

class NorthCoord:
    x=[6,8,10]
    y=[5,4,3,2,1]

class SouthCoord:
    x=[16,14,12]
    y=[19,20,21,22,23]

class EastNegCoord:
    x=[23,21,19,17,15]
    y=[13,15,17]

class WestNegCoord:
    x=[0,2,4,6,8]
    y=[11,7,9]

class NorthNegCoord:
    x=[12,14,16]
    y=[1,2,3,4,5]

class SouthNegCoord:
    x=[6,8,10]
    y=[23,22,21,20,19]



class Lane:
    def __init__(self,size):
        self.size=size
        self.Array=[0 for i in range(size)]
        self.count=0

    def getCount(self):
        return self.count
    
    def getArray(self):
        return self.Array

    def getTop(self):
        return self.Array[0]

    def pop(self):
        if self.count>0:
            carObject=self.Array[0]
            for i in range (1,self.size):
                self.Array[i-1]=self.Array[i]
            self.Array[self.size-1]=0
            self.count-=1
            return carObject

    def add(self,obj):
        if self.count<self.size:
            self.Array[self.count]=obj
            self.count+=1

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
        if lane==self.East or lane==self.West:
            if(turn==Destination.right and lane.lanePos1.getCount()<maxNumber):
                count=lane.lanePos1.getCount()
                lane.lanePos1.add(Car(type,turn,directionEnum.x[count],directionEnum.y[0]))

            elif(turn==Destination.straight):
                count=lane.lanePos1.getCount()
                if(count<maxNumber):
                    lane.lanePos1.add(Car(type,turn,directionEnum.x[count],directionEnum.y[0]))

                elif (count==maxNumber and type==VehcileType.Self_Driven and lane.lanePos3.getCount()<maxNumber):
                    count=lane.lanePos3.getCount()       
                    lane.lanePos3.add(Car(type,turn,directionEnum.x[count],directionEnum.y[2]))

            elif(turn==Destination.left and lane.lanePos2.getCount()<maxNumber):
                count=lane.lanePos2.getCount()
                lane.lanePos2.add(Car(type,turn,directionEnum.x[count],directionEnum.y[1]))



        else:
            if(turn==Destination.right and lane.lanePos1.getCount()<maxNumber):
                count=lane.lanePos1.getCount()
                lane.lanePos1.add(Car(type,turn,directionEnum.x[0],directionEnum.y[count]))

            elif(turn==Destination.straight):
                count=lane.lanePos1.getCount()
                if(count<maxNumber):
                    lane.lanePos1.add(Car(type,turn,directionEnum.x[0],directionEnum.y[count]))

                elif (count==maxNumber and type==VehcileType.Self_Driven and lane.lanePos3.getCount()<maxNumber):
                    count=lane.lanePos3.getCount()       
                    lane.lanePos3.add(Car(type,turn,directionEnum.x[2],directionEnum.y[count]))

            elif(turn==Destination.left and lane.lanePos2.getCount()<maxNumber):
                count=lane.lanePos2.getCount()
                lane.lanePos2.add(Car(type,turn,directionEnum.x[1],directionEnum.y[count]))

    

    def randomCarGenerater(self):
        origion=random.choice(list(Directions))
        turn=random.choice(list(Destination))
        type=random.choice(list(VehcileType))

        if(origion==Directions.East):
            self.addToLanes(type,turn,self.East,EastCoord)
        if(origion==Directions.North):
            self.addToLanes(type,turn,self.North,NorthCoord)
        if(origion==Directions.West):
            self.addToLanes(type,turn,self.West,WestCoord)
        if(origion==Directions.South):
            self.addToLanes(type,turn,self.South,SouthCoord)

        
    def performLeftTurn(self,origion,destination):
        if(origion.lanePos2.getSize()>0):
            destination.laneNeg2.add(origion.lanePos2.pop())

    def move(self):
        if(self.currentTrafic==Traffic.EastWest):
            #East movements
            if(self.East.lanePos1.getCount()>0):
                if(self.East.lanePos1.getTop().getDestination()==Destination.right):
                    if(self.North.laneNeg1.getCount()<maxNumber):
                        car=self.East.lanePos1.pop()
                        car.x=NorthNegCoord.x[self.North.laneNeg1.getCount()]
                        car.y=NorthNegCoord.y[0]
                        self.North.laneNeg1.add(car)

                elif(self.East.lanePos1.getTop().getDestination()==Destination.straight):
                    if self.East.lanePos1.getTop().getType()==VehcileType.Human_Driven:
                        if(self.West.laneNeg1.getCount()<maxNumber):
                            car=self.East.lanePos1.pop()
                            car.x=WestNegCoord.x[self.West.laneNeg1.getCount()]
                            car.y=WestNegCoord.y[0]
                            self.West.laneNeg1.add(car)
                    else:
                        if(self.West.laneNeg2.getCount()<maxNumber):
                            car=self.East.lanePos1.pop()
                            car.x=WestNegCoord.x[self.West.laneNeg2.getCount()]
                            car.y=WestNegCoord.y[1]
                            self.West.laneNeg2.add(car)

                elif(self.East.lanePos1.getTop().getDestination()==Destination.left):
                    if(self.North.lanePos3.getCount()<maxNumber):
                        car=self.East.lanePos1.pop()
                        car.x=NorthCoord.x[0]
                        car.y=NorthCoord.y[self.North.lanePos3.getCount()]
                        self.North.lanePos3.add(car)

            if(self.East.lanePos3.getCount()>0):
                if(self.West.laneNeg3.getCount()<maxNumber):
                    car=self.East.lanePos3.pop()
                    car.x=WestNegCoord.x[self.West.laneNeg3.getCount()]
                    car.y=WestNegCoord.y[0]
                    self.West.laneNeg3.add(car)

            #West Movements
            
        
        elif(self.currentTrafic==Traffic.NorthSouth):
            pass
            #North movements
            
            #South movements
            
        elif(self.currentTrafic==Traffic.NorthSouthLeftTurn):
            #cars turning left from North (will go east)
            self.performLeftTurn(self.North,self.South)

            #cars turning left from South (will go west)
            self.performLeftTurn(self.South,self.East)

        elif(self.currentTrafic==Traffic.EastWestLeftTurn):
            #cars turning left from east (will go south)
            self.performLeftTurn(self.East,self.South)
            
            #cars turning left from west (will go north)
            self.performLeftTurn(self.West,self.North)

    def isIn(self,x,y):
        for lane in self.fourWay:
            for innerLane in lane.lanesSet:
                for car in innerLane.getArray():
                    if(car!=0):
                        if(car.getX()==x and car.getY()==y):
                            return car   

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
                elif ((y==6 or y==18) and (x<5 or 18>x>11)):
                    print("=",end="  ")
                elif (y==12 and (1<x<8 or 20>x>14)):
                    print("-",end=" ")
                elif ((x<8 or 22>x>14) and (y==8 or y==10 or y==14 or y==16)):
                    print("--",end="")
                elif self.isIn(x,y)!=None:
                    car=self.isIn(x,y)
                    if car.getType()==VehcileType.Self_Driven:
                        print("S",end="")
                    if car.getType()==VehcileType.Human_Driven:
                        print("H",end="")
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
        sim.move()
        # sim.controlTraffic()
        # randomDelete=random.randint(0,2)
        # if randomDelete==0:
        #     sim.carsLeaving()
        time.sleep(0.5)
        #timer+=0.5
    

main()
