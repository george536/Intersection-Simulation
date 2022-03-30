import random
from enum import Enum
import time
import os


class Destination(Enum):
    East=1
    North=2
    West=3
    South=4

class Source(Enum):
    East=1
    North=2
    West=3
    South=4

class VehcileType(Enum):
    Self_Driven=0
    Human_Driven=1

class LaneType(Enum):
    rightMost=1
    middle=2
    leftMost=3

class Traffic(Enum):
    EastWest=1
    NorthSouth=2
    NorthSouthLeftTurn=3
    EastWestLeftTurn=4

class PriorityQueue:
    def __init__(self,size):
        self.size=size
        self.Array=[0 for i in range(size)]
        self.count=0
 
    
    def add(self,element):
        if(self.count<=self.size):
            for i in range(self.size):
                if(0==self.Array[i]):
                    self.Array[i]=element
                    self.count+=1
                    break

    def pop(self):
        if(self.count>0):
            out=self.Array[0]
            for i in range(1,self.count):
                self.Array[i-1]=self.Array[i]
            self.Array[self.count-1]=0
            self.count-=1
            return out

    def getArray(self):
        return self.Array[:self.count]

    def getSize(self):
        return self.count

    def getFirst(self):
        if(self.count>0):
            return self.getArray()[0]


#global vars
timer=0
maxNumber=5
timeAllocated=10
runTime=200


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
        return self.destination
    def getLane(self):
        return self.lane


class Lanes:
    global maxNumber
    def __init__(self):
        #pos means positive lane, cars are entering the intersection 
        #and exiting the lane (this is the right side of the road)
        self.lanePos1=PriorityQueue(maxNumber)
        self.lanePos2=PriorityQueue(maxNumber)
        self.lanePos3=PriorityQueue(maxNumber)
        #neg means negative lane, cars are exiting the intersection 
        #and entering the lane (this is the left side of the road)
        self.laneNeg1=PriorityQueue(maxNumber)
        self.laneNeg2=PriorityQueue(maxNumber)
        self.laneNeg3=PriorityQueue(maxNumber)

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


    def controlTraffic(self):
        global timeAllocated,timer
        if(timer==timeAllocated):
            nextTraffic=int(self.currentTrafic.value + 1)
            if nextTraffic ==5:
                nextTraffic=1
            self.currentTrafic=Traffic(nextTraffic)
            timer=0



    def canTakeMore(self,lane):
        if(len(lane.Array)<=maxNumber):
            return True
        else:
            return False

    def addToEast(self,Type,origion,destination):
        #car turning right or self-driven car turning right to go left
        if(destination==Destination.North or (destination==Destination.South and Type==VehcileType.Self_Driven)):
            if(self.canTakeMore(self.East.lanePos1)):
                self.East.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

        #Human-driven car turning left
        elif(destination==Destination.South and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.East.lanePos2)):
                self.East.lanePos2.add(Car(Type,origion,destination,LaneType.middle))

        #self-driven car going straight
        elif(destination==Destination.West and Type==VehcileType.Self_Driven):
            if(self.canTakeMore(self.East.lanePos1)):
                self.East.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

            elif(self.canTakeMore(self.East.lanePos3)):
                self.East.lanePos3.add(Car(Type,origion,destination,LaneType.leftMost))

        #human-driev car going straight
        elif(destination==Destination.West and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.East.lanePos1)):
                self.East.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

    def addToNorth(self,Type,origion,destination):
       #car turning right or self-driven car turning right to go left
        if(destination==Destination.West or (destination==Destination.West and Type==VehcileType.Self_Driven)):
            if(self.canTakeMore(self.North.lanePos1)):
                self.North.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

        #Human-driven car turning left
        elif(destination==Destination.West and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.North.lanePos2)):
                self.North.lanePos2.add(Car(Type,origion,destination,LaneType.middle))

        #self-driven car going straight
        elif(destination==Destination.South and Type==VehcileType.Self_Driven):
            if(self.canTakeMore(self.North.lanePos1)):
                self.North.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

            elif(self.canTakeMore(self.North.lanePos3)):
                self.North.lanePos3.add(Car(Type,origion,destination,LaneType.leftMost))

        #human-driev car going straight
        elif(destination==Destination.South and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.North.lanePos1)):
                self.North.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

    def addToWest(self,Type,origion,destination):
        #car turning right or self-driven car turning right to go left
        if(destination==Destination.South or (destination==Destination.North and Type==VehcileType.Self_Driven)):
            if(self.canTakeMore(self.West.lanePos1)):
                self.West.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

        #Human-driven car turning left
        elif(destination==Destination.North and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.West.lanePos2)):
                self.West.lanePos2.add(Car(Type,origion,destination,LaneType.middle))

        #self-driven car going straight
        elif(destination==Destination.South and Type==VehcileType.Self_Driven):
            if(self.canTakeMore(self.West.lanePos1)):
                self.West.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

            elif(self.canTakeMore(self.West.lanePos3)):
                self.West.lanePos3.add(Car(Type,origion,destination,LaneType.leftMost))

        #human-driev car going straight
        elif(destination==Destination.South and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.West.lanePos1)):
                self.West.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

    def addToSouth(self,Type,origion,destination):
        #car turning right or self-driven car turning right to go left
        if(destination==Destination.East or (destination==Destination.West and Type==VehcileType.Self_Driven)):
            if(self.canTakeMore(self.South.lanePos1)):
                self.South.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

        #Human-driven car turning left
        elif(destination==Destination.West and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.South.lanePos2)):
                self.South.lanePos2.add(Car(Type,origion,destination,LaneType.middle))

        #self-driven car going straight
        elif(destination==Destination.North and Type==VehcileType.Self_Driven):
            if(self.canTakeMore(self.South.lanePos1)):
                self.South.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

            elif(self.canTakeMore(self.South.lanePos3)):
                self.South.lanePos3.add(Car(Type,origion,destination,LaneType.leftMost))

        #human-driev car going straight
        elif(destination==Destination.North and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(self.South.lanePos1)):
                self.South.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost))

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

    def cleanNegLanes(self,lane):
        if lane.getSize()==maxNumber:
            lane.pop()

    def carsLeaving(self):
        for laneSet in self.fourWay:
            for i in range (3,6):
                laneSet.lanesSet[i].pop()


    def perfomeMove(self, source, rightDestination, right, straightDestination,straight, 
    leftSelfDrivenDestination,leftSelfDriven, HumanDrivenOnLeftGoingStraight):
        if(source.lanePos1.getSize()>0):
            if(source.lanePos1.getFirst().getDestination()==rightDestination):
                self.cleanNegLanes(right.laneNeg1)
                right.laneNeg1.add(source.lanePos1.pop())

            elif(source.lanePos1.getFirst().getDestination()==straightDestination):
                if(source.lanePos1.getFirst().isSelfDriven()==VehcileType.Human_Driven):
                    self.cleanNegLanes(straight.laneNeg1)
                    straight.laneNeg1.add(source.lanePos1.pop())

                elif (source.lanePos1.getFirst().isSelfDriven()==VehcileType.Self_Driven):
                    self.cleanNegLanes(straight.laneNeg2)
                    straight.laneNeg2.add(source.lanePos1.pop())

            elif(source.lanePos1.getFirst().getDestination()==leftSelfDrivenDestination):
                if(self.canTakeMore(leftSelfDriven.lanePos3)):
                    temp=source.lanePos1.pop()
                    temp.lane=LaneType.leftMost
                    leftSelfDriven.lanePos3.add(temp)

        if(source.lanePos3.getSize()>0):
            self.cleanNegLanes(HumanDrivenOnLeftGoingStraight.laneNeg3)
            HumanDrivenOnLeftGoingStraight.laneNeg3.add(source.lanePos3.pop())


    def move(self):
        self.update()
        if(self.currentTrafic==Traffic.EastWest):
            #East movements
            self.perfomeMove(self.East,Destination.North,self.North,Destination.West,self.West,Destination.South,self.North,self.West)

            #West Movements
            self.perfomeMove(self.West,Destination.South,self.South,Destination.East,self.East,Destination.North,self.South,self.East)

        
        elif(self.currentTrafic==Traffic.NorthSouth):
            #North movements
            self.perfomeMove(self.North,Destination.West,self.West,Destination.South,self.South,Destination.East,self.West,self.South)

            
            #South movements
            if(self.South.lanePos1.getSize()>0):
                if(self.South.lanePos1.getFirst().getDestination()==Destination.East):
                    self.cleanNegLanes(self.East.laneNeg1)
                    self.East.laneNeg1.add(self.South.lanePos1.pop())

                elif(self.South.lanePos1.getFirst().getDestination()==Destination.North):
                    if(self.South.lanePos1.getFirst().isSelfDriven()==VehcileType.Human_Driven):
                        self.cleanNegLanes(self.North.laneNeg1)
                        self.North.laneNeg1.add(self.South.lanePos1.pop())

                    elif(self.South.lanePos1.getFirst().isSelfDriven()==VehcileType.Self_Driven):
                        self.cleanNegLanes(self.North.laneNeg2)
                        self.North.laneNeg2.add(self.South.lanePos1.pop())

                elif(self.South.lanePos1.getFirst().getDestination()==Destination.West):
                    if(self.canTakeMore(self.East.lanePos3)):
                        temp=self.South.lanePos1.pop()
                        temp.lane=LaneType.leftMost
                        self.East.lanePos3.add(temp)

            if(self.South.lanePos3.getSize()>0):
                self.cleanNegLanes(self.South.laneNeg3)
                self.North.laneNeg3.add(self.South.lanePos3.pop())


        elif(self.currentTrafic==Traffic.NorthSouthLeftTurn):
            #cars turning left from North (will go east)
            if(self.North.lanePos2.getSize()>0):
                self.cleanNegLanes(self.East.laneNeg2)
                self.East.laneNeg2.add(self.North.lanePos2.pop())

            #cars turning left from South (will go west)
            if(self.South.lanePos2.getSize()>0):
                self.cleanNegLanes(self.West.laneNeg2)
                self.West.laneNeg2.add(self.South.lanePos2.pop())
            

        elif(self.currentTrafic==Traffic.EastWestLeftTurn):
            #cars turning left from east (will go south)
            if(self.East.lanePos2.getSize()>0):
                self.cleanNegLanes(self.South.laneNeg2)
                self.South.laneNeg2.add(self.East.lanePos2.pop())

            #cars turning left from west (will go north)
            if(self.West.lanePos2.getSize()>0):
                self.cleanNegLanes(self.North.laneNeg2)
                self.North.laneNeg2.add(self.West.lanePos2.pop())

        self.update()

        
    def draw(self):
        os.system('cls')
        self.update()
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
                    print("",end=" ")
                elif (y==12 and (1<x<7 or 20>x>14)):
                    print("-",end=" ")
                elif ((x<7 or 22>x>14) and (y==8 or y==10 or y==14 or y==16)):
                    print("--",end="")
                elif(y>5 and y<19):
                    print(" ",end=" ")
                else:
                    print(" ",end="") 
            print("")

    def display(self):

        os.system('cls')
        self.update()
        print("East\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            if(self.East.lanesSet[i].getSize()>0):
                for car in self.East.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")

        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            if(self.East.lanesSet[i].getSize()>0):
                for car in self.East.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")

        print("North\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            if(self.North.lanesSet[i].getSize()>0):
                for car in self.North.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")
        
        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            if(self.North.lanesSet[i].getSize()>0):
                for car in self.North.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")
        
        print("West\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            if(self.West.lanesSet[i].getSize()>0):
                for car in self.West.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")

        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            if(self.West.lanesSet[i].getSize()>0):
                for car in self.West.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")

        print("South\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            if(self.South.lanesSet[i].getSize()>0):
                for car in self.South.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")
        
        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            if(self.South.lanesSet[i].getSize()>0):
                for car in self.South.lanesSet[i].getArray():
                    print("car ",car.getDestination(),end=" ")
            print("\n")
        


def main():

    sim = Intersection()
    sim.currentTrafic=Traffic.EastWest
    
    global timer,timeAllocated, runTime
    timer=0
    timePassed=0
    while(timePassed<=runTime):    
        sim.display()
        sim.randomCarGenerater()
        print(sim.currentTrafic)
        sim.move()
        sim.controlTraffic()
        randomDelete=random.randint(0,2)
        if randomDelete==0:
            sim.carsLeaving()
        time.sleep(0.1)
        timer+=0.5
    

main()
