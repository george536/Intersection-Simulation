import random
from enum import Enum
import time
import os

#hi

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
    def __init__(self,Type, source, destination, lane, x, y):
        self.Type=Type
        self.source=source
        self.destination=destination
        self.lane=lane
        self.x=x
        self.y=y

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
        if(lane.getSize()<maxNumber):
            return True
        else:
            return False

    def sortCarsInLanes(self, source, origion, Type, destination, right, straight, left, x, y):
        #car turning right or self-driven car turning right to go left
        if(destination==right or (destination==left and Type==VehcileType.Self_Driven)):
            if(self.canTakeMore(source.lanePos1)):
                source.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost, x[source.lanePos1.getSize()], y[0]))

        #Human-driven car turning left
        elif(destination==left and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(source.lanePos2)):
                source.lanePos2.add(Car(Type,origion,destination,LaneType.middle, x[source.lanePos2.getSize()], y[1]))

        #self-driven car going straight
        elif(destination==straight and Type==VehcileType.Self_Driven):
            if(self.canTakeMore(source.lanePos1)):
                source.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost, x[source.lanePos1.getSize()], y[0]))

            elif(self.canTakeMore(source.lanePos3)):
                source.lanePos3.add(Car(Type,origion,destination,LaneType.leftMost, x[source.lanePos3.getSize()], y[2]))

        #human-driev car going straight
        elif(destination==straight and Type==VehcileType.Human_Driven):
            if(self.canTakeMore(source.lanePos1)):
                source.lanePos1.add(Car(Type,origion,destination,LaneType.rightMost, x[source.lanePos1.getSize()], y[0]))


    def randomCarGenerater(self):
        origion=random.choice(list(Source))
        destination=random.choice(list(Destination))
        Type=random.choice(list(VehcileType))

        if(destination.value!=origion.value):
            if(origion==Source.East):
                self.sortCarsInLanes(self.East,origion,Type, destination,Destination.North,Destination.West,Destination.South,[15,17,19,21,23],[7,9,11])
            # if(origion==Source.North):
            #     self.sortCarsInLanes(self.North,origion,Type, destination,Destination.West, Destination.South, Destination.East)
            # if(origion==Source.West):
            #     self.sortCarsInLanes(self.West,origion,Type, destination,Destination.South,Destination.East,Destination.North)
            # if(origion==Source.South):
            #     self.sortCarsInLanes(self.South,origion,Type, destination,Destination.East,Destination.North,Destination.West)



    def cleanNegLanes(self,lane):
        if lane.getSize()==maxNumber:
            lane.pop()

    def carsLeaving(self):
        self.update()
        for laneSet in self.fourWay:
            for i in range (3,6):
                laneSet.lanesSet[i].pop()


    def perfomMove(self, source, rightDestination, right, straightDestination,straight, 
    leftSelfDrivenDestination,leftSelfDriven, HumanDrivenOnLeftGoingStraight,x,y):
        if(source.lanePos1.getSize()>0):
            if(source.lanePos1.getFirst().getDestination()==rightDestination):
                self.cleanNegLanes(right.laneNeg1)
                car=source.lanePos1.pop()
                car.x=x[right.laneNeg1.getSize()]
                right.laneNeg1.add(car)

            elif(source.lanePos1.getFirst().getDestination()==straightDestination):
                if(source.lanePos1.getFirst().isSelfDriven()==VehcileType.Human_Driven):
                    self.cleanNegLanes(straight.laneNeg1)
                    car=source.lanePos1.pop()
                    car.x=x[straight.laneNeg1.getSize()]
                    straight.laneNeg1.add(car)

                elif (source.lanePos1.getFirst().isSelfDriven()==VehcileType.Self_Driven):
                    self.cleanNegLanes(straight.laneNeg2)
                    car=source.lanePos1.pop()
                    car.x=x[straight.laneNeg2.getSize()]
                    car.y=y[1]
                    straight.laneNeg2.add(car)

            elif(source.lanePos1.getFirst().getDestination()==leftSelfDrivenDestination):
                if(self.canTakeMore(leftSelfDriven.lanePos3)):
                    temp=source.lanePos1.pop()
                    temp.lane=LaneType.leftMost
                    leftSelfDriven.lanePos3.add(temp)

        if(source.lanePos3.getSize()>0):
            self.cleanNegLanes(HumanDrivenOnLeftGoingStraight.laneNeg3)
            car=source.lanePos3.pop()
            car.x=x[HumanDrivenOnLeftGoingStraight.laneNeg3.getSize()]
            HumanDrivenOnLeftGoingStraight.laneNeg3.add(car)



    def performLeftTurn(self,origion,destination):
        if(origion.lanePos2.getSize()>0):
                self.cleanNegLanes(destination.laneNeg2)
                destination.laneNeg2.add(origion.lanePos2.pop())


    def move(self):
        if(self.currentTrafic==Traffic.EastWest):
            #East movements
            self.perfomMove(self.East,Destination.North,self.North,Destination.West,self.West,Destination.South,self.North,self.West,[0,1,2,3,4],[7,9,11])
            for car in self.East.lanePos1.getArray():
                if(self.East.lanePos1.getSize()>=0):
                    car.x=car.x-2
            for car in self.East.lanePos3.getArray():
                if(self.East.lanePos3.getSize()>=0):
                    car.x=car.x-2

            #West Movements
            #self.perfomMove(self.West,Destination.South,self.South,Destination.East,self.East,Destination.North,self.South,self.East)

        
        elif(self.currentTrafic==Traffic.NorthSouth):
            pass
            #North movements
            #self.perfomMove(self.North,Destination.West,self.West,Destination.South,self.South,Destination.East,self.West,self.South)

            
            #South movements
            #self.perfomMove(self.South,Destination.East,self.East,Destination.North,self.North,Destination.West,self.East,self.North)


        elif(self.currentTrafic==Traffic.NorthSouthLeftTurn):
            pass
            #cars turning left from North (will go east)
            #self.performLeftTurn(self.North,self.East)

            #cars turning left from South (will go west)
            #self.performLeftTurn(self.South,self.West)

        elif(self.currentTrafic==Traffic.EastWestLeftTurn):
            #cars turning left from east (will go south)
            self.performLeftTurn(self.East,self.South)

            #cars turning left from west (will go north)
            self.performLeftTurn(self.West,self.North)


    def isIn(self,x,y):
        for lane in self.fourWay:
            for innerLane in lane.lanesSet:
                for car in innerLane.getArray():
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

    #temporary
    def display(self):

        os.system('cls')
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
        sim.draw()
        sim.randomCarGenerater()
        print(sim.currentTrafic)
        sim.move()
        sim.controlTraffic()
        randomDelete=random.randint(0,2)
        if randomDelete==0:
            sim.carsLeaving()
        time.sleep(0.3)
        timer+=0.5
    

main()
