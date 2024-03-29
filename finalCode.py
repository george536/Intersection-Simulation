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
    EastWestLeftTurn=3
    NorthSouthLeftTurn=4
    

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
    #x=[23,21,19,17,15]
    x=[15,17,19,21,23]
    #y=[13,15,17]
    y=[17,15,13]
class WestNegCoord:
    
    x=[8,6,4,2,0]
    #x=[0,2,4,6,8]
    #y=[11,7,9]
    y=[7,9,11]
class NorthNegCoord:
    x=[16,14,12]
    #y=[1,2,3,4,5]
    y=[5,4,3,2,1]

class SouthNegCoord:
    x=[6,8,10]
    #y=[23,22,21,20,19]
    y=[19,20,21,22,23]



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
timeAllocated=5

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

    def controlTraffic(self):
        global timeAllocated,timer
        #if(timer==timeAllocated):
        if(timer%timeAllocated==0 and timer!=0):
            nextTraffic=int(self.currentTrafic.value + 1)
            if nextTraffic ==5:
                nextTraffic=1
            self.currentTrafic=Traffic(nextTraffic)

        if self.currentTrafic==Traffic.EastWestLeftTurn and self.East.lanePos2.getCount()==0 and self.West.lanePos2.getCount()==0:
            self.currentTrafic=Traffic.NorthSouthLeftTurn
            timer=0
        elif self.currentTrafic==Traffic.NorthSouthLeftTurn and self.South.lanePos2.getCount()==0 and self.North.lanePos2.getCount()==0:
            self.currentTrafic=Traffic.EastWest
            timer=0

    def addToLanes(self,type,turn,lane,directionEnum):
        global maxNumber
        if lane==self.East or lane==self.West:
            if((turn==Destination.right and lane.lanePos1.getCount()<maxNumber) or (turn==Destination.left and lane.lanePos1.getCount()<maxNumber and type==VehcileType.Self_Driven)):
                count=lane.lanePos1.getCount()
                lane.lanePos1.add(Car(type,turn,directionEnum.x[count],directionEnum.y[0]))

            elif(turn==Destination.straight):
                count=lane.lanePos1.getCount()
                if(count<maxNumber):
                    lane.lanePos1.add(Car(type,turn,directionEnum.x[count],directionEnum.y[0]))

                elif (count==maxNumber and type==VehcileType.Self_Driven and lane.lanePos3.getCount()<maxNumber):
                    count=lane.lanePos3.getCount()       
                    lane.lanePos3.add(Car(type,turn,directionEnum.x[count],directionEnum.y[2]))

            elif(turn==Destination.left and lane.lanePos2.getCount()<maxNumber and type==VehcileType.Human_Driven):
                count=lane.lanePos2.getCount()
                lane.lanePos2.add(Car(type,turn,directionEnum.x[count],directionEnum.y[1]))



        else:
            if((turn==Destination.right and lane.lanePos1.getCount()<maxNumber) or (turn==Destination.left and lane.lanePos1.getCount()<maxNumber and type==VehcileType.Self_Driven)):
                count=lane.lanePos1.getCount()
                lane.lanePos1.add(Car(type,turn,directionEnum.x[0],directionEnum.y[count]))

            elif(turn==Destination.straight):
                count=lane.lanePos1.getCount()
                if(count<maxNumber):
                    lane.lanePos1.add(Car(type,turn,directionEnum.x[0],directionEnum.y[count]))

                elif (count==maxNumber and type==VehcileType.Self_Driven and lane.lanePos3.getCount()<maxNumber):
                    count=lane.lanePos3.getCount()       
                    lane.lanePos3.add(Car(type,turn,directionEnum.x[2],directionEnum.y[count]))

            elif(turn==Destination.left and lane.lanePos2.getCount()<maxNumber and type==VehcileType.Human_Driven):
                count=lane.lanePos2.getCount()
                lane.lanePos2.add(Car(type,turn,directionEnum.x[1],directionEnum.y[count]))

    

    def randomCarGenerater(self):
        origion=random.choice(list(Directions))
        #origion=Directions.West
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

        
    def performLeftTurn(self,origion,destination,destCoord):
        if(origion.lanePos2.getCount()>0 and destination.laneNeg2.getCount()<maxNumber and (origion==self.East or origion==self.West)):
            car=origion.lanePos2.pop()
            self.shift(origion,origion.lanePos2.getArray())
            car.x=destCoord.x[1]
            car.y=destCoord.y[destination.laneNeg2.getCount()]
            destination.laneNeg2.add(car)
        elif(origion.lanePos2.getCount()>0 and destination.laneNeg2.getCount()<maxNumber and (origion==self.South or origion==self.North)):
            car=origion.lanePos2.pop()
            self.shift(origion,origion.lanePos2.getArray())
            car.x=destCoord.x[destination.laneNeg2.getCount()]
            car.y=destCoord.y[1]
            destination.laneNeg2.add(car)


    def shift(self,source,lane):
        if source==self.East:
            for car in lane:
                if car!=0:car.x-=2
        if source==self.West:
            for car in lane:
                if car!=0:car.x+=2
        if source==self.North:
            for car in lane:
                if car!=0:car.y+=1
        if source==self.South:
            for car in lane:
                if car!=0:car.y-=1

    def performMove(self,source,rightLane,StraightLane,rightNegCoord,rightCoord,straightNegCoord):
        if source==self.East or source==self.West:
            if(source.lanePos1.getCount()>0):
                    if(source.lanePos1.getTop().getDestination()==Destination.right):
                        if(rightLane.laneNeg1.getCount()<maxNumber):
                            car=source.lanePos1.pop()
                            self.shift(source,source.lanePos1.getArray())
                            car.x=rightNegCoord.x[0]
                            car.y=rightNegCoord.y[rightLane.laneNeg1.getCount()]
                            rightLane.laneNeg1.add(car)

                    elif(source.lanePos1.getTop().getDestination()==Destination.straight):
                        if source.lanePos1.getTop().getType()==VehcileType.Human_Driven:
                            if(StraightLane.laneNeg1.getCount()<maxNumber):
                                car=source.lanePos1.pop()
                                self.shift(source,source.lanePos1.getArray())
                                car.x=straightNegCoord.x[StraightLane.laneNeg1.getCount()]
                                car.y=straightNegCoord.y[0]
                                StraightLane.laneNeg1.add(car)
                        else:
                            if(StraightLane.laneNeg2.getCount()<maxNumber):
                                car=source.lanePos1.pop()
                                self.shift(source,source.lanePos1.getArray())
                                car.x=straightNegCoord.x[StraightLane.laneNeg2.getCount()]
                                car.y=straightNegCoord.y[1]
                                StraightLane.laneNeg2.add(car)

                    elif(source.lanePos1.getTop().getDestination()==Destination.left):
                        if(rightLane.lanePos3.getCount()<maxNumber):
                            car=source.lanePos1.pop()
                            self.shift(source,source.lanePos1.getArray())
                            car.x=rightCoord.x[2]
                            car.y=rightCoord.y[rightLane.lanePos3.getCount()]
                            rightLane.lanePos3.add(car)
            
            if(source.lanePos3.getCount()>0):
                if(StraightLane.laneNeg3.getCount()<maxNumber):
                    car=source.lanePos3.pop()
                    self.shift(source,source.lanePos3.getArray())
                    car.x=straightNegCoord.x[StraightLane.laneNeg3.getCount()]
                    car.y=straightNegCoord.y[0]
                    StraightLane.laneNeg3.add(car)
        else:
            if(source.lanePos1.getCount()>0):
                    if(source.lanePos1.getTop().getDestination()==Destination.right):
                        if(rightLane.laneNeg1.getCount()<maxNumber):
                            car=source.lanePos1.pop()
                            self.shift(source,source.lanePos1.getArray())
                            car.x=rightNegCoord.x[rightLane.laneNeg1.getCount()]
                            car.y=rightNegCoord.y[0]
                            rightLane.laneNeg1.add(car)

                    elif(source.lanePos1.getTop().getDestination()==Destination.straight):
                        if source.lanePos1.getTop().getType()==VehcileType.Human_Driven:
                            if(StraightLane.laneNeg1.getCount()<maxNumber):
                                car=source.lanePos1.pop()
                                self.shift(source,source.lanePos1.getArray())
                                car.x=straightNegCoord.x[0]
                                car.y=straightNegCoord.y[StraightLane.laneNeg1.getCount()]
                                StraightLane.laneNeg1.add(car)
                        else:
                            if(StraightLane.laneNeg2.getCount()<maxNumber):
                                car=source.lanePos1.pop()
                                self.shift(source,source.lanePos1.getArray())
                                car.x=straightNegCoord.x[1]
                                car.y=straightNegCoord.y[StraightLane.laneNeg2.getCount()]
                                StraightLane.laneNeg2.add(car)

                    elif(source.lanePos1.getTop().getDestination()==Destination.left):
                        if(rightLane.lanePos3.getCount()<maxNumber):
                            car=source.lanePos1.pop()
                            self.shift(source,source.lanePos1.getArray())
                            car.x=rightCoord.x[rightLane.lanePos3.getCount()]
                            car.y=rightCoord.y[2]
                            rightLane.lanePos3.add(car)
            
            if(source.lanePos3.getCount()>0):
                if(StraightLane.laneNeg3.getCount()<maxNumber):
                    car=source.lanePos3.pop()
                    self.shift(source,source.lanePos3.getArray())
                    car.x=straightNegCoord.x[0]
                    car.y=straightNegCoord.y[StraightLane.laneNeg3.getCount()]
                    StraightLane.laneNeg3.add(car)

    def move(self):
        if(self.currentTrafic==Traffic.EastWest):
            #East movements
            self.performMove(self.East, self.North, self.West, NorthNegCoord,NorthCoord, WestNegCoord)
            #West Movements
            self.performMove(self.West, self.South, self.East, SouthNegCoord, SouthCoord,EastNegCoord)
        
        elif(self.currentTrafic==Traffic.NorthSouth):
            pass
            #North movements
            self.performMove(self.North, self.West, self.South, WestNegCoord,WestCoord, SouthNegCoord)
            #South movements
            self.performMove(self.South, self.East, self.North, EastNegCoord,EastCoord, NorthNegCoord)

        elif(self.currentTrafic==Traffic.NorthSouthLeftTurn):
            #cars turning left from North (will go east)
            self.performLeftTurn(self.North,self.East,EastNegCoord)

            #cars turning left from South (will go west)
            self.performLeftTurn(self.South,self.West,WestNegCoord)

        elif(self.currentTrafic==Traffic.EastWestLeftTurn):
            #cars turning left from east (will go south)
            self.performLeftTurn(self.East,self.South,SouthNegCoord)
            
            #cars turning left from west (will go north)
            self.performLeftTurn(self.West,self.North, NorthNegCoord)


    def clearNegativeLanes(self):
        for i in range(3,6):
            for car in self.East.lanesSet[i].getArray():
                if car!=0:
                    car.x+=2
                    if car.x>=24:
                        self.East.lanesSet[i].pop()


            for car in self.North.lanesSet[i].getArray():
                if car!=0:
                    car.y-=1
                    if(car.y<=0):
                        self.North.lanesSet[i].pop()
                
            for car in self.South.lanesSet[i].getArray():
                if car!=0:
                    car.y+=1
                    if(car.y>=24):
                        self.South.lanesSet[i].pop()
            
            for car in self.West.lanesSet[i].getArray():
                if car!=0:
                    car.x-=2
                    if car.x<=0:
                        self.West.lanesSet[i].pop()


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
                elif (y==12 and (1<x<8 or 20>x>13)):
                    print("-",end=" ")
                elif ((x<8 or 22>x>13) and (y==8 or y==10 or y==14 or y==16)):
                    print("--",end="")
                #extra
                elif (y>5 and y<19 and x>8 and x<14):
                    print(" ",end=" ")
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

    def carsAvg(self):
        sum=0
        list=[0,2]
        for i in list:
            if self.currentTrafic!=Traffic.EastWest:
                sum+=self.East.lanesSet[i].getCount()
                sum+=self.West.lanesSet[i].getCount()
            if self.currentTrafic!=Traffic.NorthSouth:
                sum+=self.South.lanesSet[i].getCount()
                sum+=self.North.lanesSet[i].getCount()
        if self.currentTrafic!=Traffic.NorthSouthLeftTurn:
            sum+=self.South.lanesSet[1].getCount()
            sum+=self.North.lanesSet[1].getCount()
        if self.currentTrafic!=Traffic.EastWestLeftTurn:
            sum+=self.East.lanesSet[1].getCount()
            sum+=self.West.lanesSet[1].getCount()
        return sum/12

def main():

    sim = Intersection()
    sim.currentTrafic=Traffic.EastWest
    
    global timer, timeAllocated
    timeAllocated = 5
    timer=0
    while(True):    
        sim.draw()
        sim.randomCarGenerater()
        # sim.randomCarGenerater()
        # sim.randomCarGenerater()
        # sim.randomCarGenerater()
        # sim.randomCarGenerater()
        # sim.randomCarGenerater()
        print(sim.currentTrafic)
        sim.update()
        sim.move()
        sim.controlTraffic()
        time.sleep(0.5)
        sim.clearNegativeLanes()
        timer+=0.5


main()
