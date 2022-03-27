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
        self.currentTrafic=currentTrafic

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

        self.currentTrafic=currentTrafic

    def controlTraffic(self):
        global currentTrafic
        #put code here
        self.currentTrafic=currentTrafic
        pass

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

    def move(self):
        self.update()
        if(self.currentTrafic==Traffic.EastWest):
            #East movements
            if(self.East.lanePos1.getSize()>0):
                if(self.East.lanePos1.getFirst().getDestination()==Destination.North):
                    self.cleanNegLanes(self.North.laneNeg1)
                    self.North.laneNeg1.add(self.East.lanePos1.pop())
                elif(self.East.lanePos1.getFirst().getDestination()==Destination.West):
                    if(self.East.lanePos1.getFirst().isSelfDriven==VehcileType.Human_Driven):
                        self.cleanNegLanes(self.West.laneNeg1)
                        self.West.laneNeg1.add(self.East.lanePos1.pop())
                    elif (self.East.lanePos1.getFirst().isSelfDriven==VehcileType.Self_Driven):
                        self.cleanNegLanes(self.West.laneNeg2)
                        self.West.laneNeg2.add(self.East.lanePos1.pop())
                elif(self.East.lanePos1.getFirst().getDestination()==Destination.South):
                    if(self.canTakeMore(self.North.lanePos3)):
                        temp=self.East.lanePos1.pop()
                        temp.lane=LaneType.leftMost
                        self.North.lanePos3.add(temp)

            if(self.East.lanePos3.getSize()>0):
                self.cleanNegLanes(self.West.laneNeg3)
                self.West.laneNeg3.add(self.East.lanePos3.pop())

            #West Movements
            if(self.West.lanePos1.getSize()>0):
                if(self.West.lanePos1.getFirst().getDestination()==Destination.South):
                    self.cleanNegLanes(self.South.laneNeg1)
                    self.South.laneNeg1.add(self.West.lanePos1.pop())
                elif(self.West.lanePos1.getFirst().getDestination()==Destination.East):
                    if(self.West.lanePos1.getFirst().isSelfDriven==VehcileType.Human_Driven):
                        self.cleanNegLanes(self.East.laneNeg1)
                        self.East.laneNeg1.add(self.West.lanePos1.pop())
                    elif(self.West.lanePos1.getFirst().isSelfDriven==VehcileType.Self_Driven):
                        self.cleanNegLanes(self.East.laneNeg2)
                        self.East.laneNeg2.add(self.West.lanePos1.pop())
                elif(self.West.lanePos1.getFirst().getDestination()==Destination.North):
                    if(self.canTakeMore(self.South.lanePos3)):
                        temp=self.West.lanePos1.pop()
                        temp.lane=LaneType.leftMost
                        self.South.lanePos3.add(temp)

            if(self.West.lanePos3.getSize()>0):
                self.cleanNegLanes(self.East.laneNeg3)
                self.East.laneNeg3.add(self.West.lanePos3.pop())

        
        if(self.currentTrafic==Traffic.NorthSouth):
            #North movements
            if(self.North.lanePos1.getSize()>0):
                if(self.North.lanePos1.getFirst().getDestination()==Destination.West):
                    self.cleanNegLanes(self.West.laneNeg1)
                    self.West.laneNeg1.add(self.North.lanePos1.pop())
                elif(self.North.lanePos1.getFirst().getDestination()==Destination.South):
                    self.cleanNegLanes(self.South.laneNeg1)
                    self.South.laneNeg1.add(self.North.lanePos1.pop())
                elif(self.East.lanePos1.getFirst().getDestination()==Destination.South):
                    if(self.canTakeMore(self.North.lanePos3)):
                        temp=self.East.lanePos1.pop()
                        temp.lane=LaneType.leftMost
                        self.North.lanePos3.add(temp)

            if(self.East.lanePos3.getSize()>0):
                self.cleanNegLanes(self.West.laneNeg3)
                self.West.laneNeg3.add(self.East.lanePos3.pop())


        self.update()
            

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
        self.update()
        # for laneSet in self.fourWay:
        #     for lane in laneSet.lanesSet:
        #         for car in lane.getArray():
        #             print("Is it self-driven: ",car.isSelfDriven(),"\nSource: ",car.getSource(),"\ndestination: ",car.getDestination(), "\nin lane: ", car.getLane(),"\n")
        print("East\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            for car in self.East.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")

        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            for car in self.East.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")

        print("North\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            for car in self.North.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")

        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            for car in self.North.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")

        print("West\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            for car in self.West.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")

        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            for car in self.West.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")

        print("South\n")
        for i in range(3):
            print("Pos",i+1,"lane: ",end="")
            for car in self.South.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")

        print("\n")

        for i in range(3,6):
            print("Neg",i-3+1,"lane: ",end="")
            for car in self.South.lanesSet[i].getArray():
                print("car ",car.getDestination(),end=" ")
            print("\n")


def main():
    sim = Intersection()
    i=0
    while(i<50):
        sim.randomCarGenerater()
        i+=1
    sim.display()

    print("------------------------------------------")
    sim.move()
    print("------------------------------------------")
    sim.display()

    #print(sim.West.laneNeg1.pop().getSource())

main()
