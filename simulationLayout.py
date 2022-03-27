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

    def getFirst(self):
        if (self.count > 0): 
            first = self.Array[0]
        return first

    def getArray(self):
        return self.Array[:self.count]

    def getSize(self):
        return self.count

    def getTop(self):
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

    def move(self):
        self.update()
        if(self.currentTrafic==Traffic.EastWest):
            if()

            '''
            #loop over PQ (positive ones) from east and west
            for i in range(3):
                #East lanes
                for vehicle in self.East.lanesSet[i].getArray():
                    #cars that are going straight
                    if(vehicle.getDestination()==Destination.West):
                        #let self driven vehicles going straight switch to middle lane
                        if(vehicle.getLane()==LaneType.rightMost and vehicle.isSelfDriven()==VehcileType.Self_Driven):
                            self.West.laneNeg2.add(self.East.lanesSet[i].pop())
                        #let human driven cars going straight stay in right most lane
                        elif (vehicle.getLane()==LaneType.rightMost and vehicle.isSelfDriven()==VehcileType.Human_Driven):
                            self.West.laneNeg1.add(self.East.lanesSet[i].pop())
                        #let cars in left most lane going straight still go straight
                        elif (vehicle.getLane()==LaneType.leftMost):
                            self.West.laneNeg3.add(self.East.lanesSet[i].pop())

                    #self driven cars in right lane going right in order to turn left later
                    if(vehicle.getDestination()==Destination.South and vehicle.getLane()==LaneType.rightMost and vehicle.isSelfDriven()==VehcileType.Self_Driven):
                        if(self.canTakeMore(self.North.lanePos3)):
                            self.North.lanePos3.add(self.East.lanesSet[i].pop())

                    #cars in right lane turning right (self driven or human)
                    if (vehicle.getDestination()==Destination.North and vehicle.getLane()==LaneType.rightMost):
                        self.North.laneNeg1.add(self.East.lanesSet[i].pop())
                

                #West lanes 
                for vehicle in self.West.lanesSet[i].getArray():
                    #cars going straight
                    if(vehicle.getDestination()==Destination.East and (vehicle.getLane()==LaneType.rightMost or vehicle.getLane()==LaneType.leftMost)):
                        self.East.laneNeg1.add(self.West.lanesSet[i].pop())

                    #self-driven cars in right lane going right in order to turn left later
                    if(vehicle.getDestination()==Destination.North and vehicle.getLane()==LaneType.rightMost and vehicle.isSelfDriven()==VehcileType.Self_Driven):
                        if(self.canTakeMore(self.South.lanePos3)):
                            self.South.lanePos3.add(self.West.lanesSet[i].pop())
                    
                    #cars in right lane turning right (self driven or human)
                    if (vehicle.getDestination()==Destination.South and vehicle.getLane()==LaneType.rightMost):
                        self.South.laneNeg1.add(self.West.lanesSet[i].pop())

        if (self.currentTrafic==Traffic.NorthSouth):
            #loop over pos PQs from North and South
            for j in range(3):
                #North lanes
                for vehicle in self.North.lanesSet[i].getArray():
                    #cars going straight
                    if(vehicle.getDestination()==Destination.South and (vehicle.getLane()==LaneType.rightMost or vehicle.getLane()==LaneType.leftMost)):
                        self.South.laneNeg1.add(self.North.lanesSet[i].pop())

                    #self-driven cars in right lane going right in order to turn left later
                    if(vehicle.getDestination()==Destination.East and vehicle.getLane()==LaneType.rightMost and vehicle.isSelfDriven()==VehcileType.Self_Driven):
                        if(self.canTakeMore(self.West.lanePos3)):
                            self.West.lanePos3.add(self.North.lanesSet[i].pop())
                    
                    #cars in right lane turning right (self driven or human)
                    if (vehicle.getDestination()==Destination.West and vehicle.getLane()==LaneType.rightMost):
                        self.West.laneNeg1.add(self.North.lanesSet[i].pop())
                
                #South lanes
                for vehicle in self.South.lanesSet[i].getArray():
                     #cars going straight
                    if(vehicle.getDestination()==Destination.North and (vehicle.getLane()==LaneType.rightMost or vehicle.getLane()==LaneType.leftMost)):
                        self.North.laneNeg1.add(self.South.lanesSet[i].pop())

                    #self-driven cars in right lane going right in order to turn left later
                    if(vehicle.getDestination()==Destination.West and vehicle.getLane()==LaneType.rightMost and vehicle.isSelfDriven()==VehcileType.Self_Driven):
                        if(self.canTakeMore(self.East.lanePos3)):
                            self.East.lanePos3.add(self.South.lanesSet[i].pop())
                    
                    #cars in right lane turning right (self driven or human)
                    if (vehicle.getDestination()==Destination.East and vehicle.getLane()==LaneType.rightMost):
                        self.East.laneNeg1.add(self.South.lanesSet[i].pop())

        if (self.currentTrafic==Traffic.EastWestLeftTurn):
            #East lanes 
            #human-driven cars making left turn from middle
            for vehicle in self.East.lanePos2.getArray():
                self.South.laneNeg2.add(self.East.lanePos2.pop())
            
            #cars making a right turn (only human)
            firstVehicle = self.East.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Human_Driven):
                self.North.laneNeg1.add(self.East.lanePos1.pop())
                firstVehicle = self.East.lanePos1.getFirst()

            #West lanes
            #human-driven cars making left turn from middle
            for vehicle in self.West.lanePos2.getArray():
                self.North.laneNeg2.add(self.West.lanePos2.pop())

            #cars making a right turn (only human)
            firstVehicle = self.West.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Human_Driven):
                self.South.laneNeg1.add(self.West.lanePos1.pop())
                firstVehicle = self.West.lanePos1.getFirst()

            #North lanes
            #cars making right turn to make u-turn
            firstVehicle = self.North.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Self_Driven and firstVehicle.getDestination()==Destination.East):
                if (self.canTakeMore(self.West.lanePos3)):
                    self.West.lanePos3.add(self.North.lanePos1.pop())
                else: break
                firstVehicle = self.North.lanePos1.getFirst()

            #South lanes
            #cars making right turn to make u-turn
            firstVehicle = self.South.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Self_Driven and firstVehicle.getDestination()==Destination.West):
                if (self.canTakeMore(self.East.lanePos3)):
                    self.East.lanePos3.add(self.South.lanePos1.pop())
                else: break
                firstVehicle = self.South.lanePos1.getFirst()

        if (self.currentTrafic==Traffic.NorthSouthLeftTurn):
            #North lanes 
            #human-driven cars making left turn from middle
            for vehicle in self.North.lanePos2.getArray():
                self.East.laneNeg2.add(self.North.lanePos2.pop())
            
            #cars making a right turn (only human)
            firstVehicle = self.North.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Human_Driven):
                self.West.laneNeg1.add(self.North.lanePos1.pop())
                firstVehicle = self.North.lanePos1.getFirst()

            #South lanes
            #human-driven cars making left turn from middle
            for vehicle in self.South.lanePos2.getArray():
                self.West.laneNeg2.add(self.South.lanePos2.pop())

            #cars making a right turn (only human)
            firstVehicle = self.South.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Human_Driven):
                self.East.laneNeg1.add(self.South.lanePos1.pop())
                firstVehicle = self.South.lanePos1.getFirst()

            #East lanes
            #cars making right turn to make u-turn
            firstVehicle = self.East.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Self_Driven and firstVehicle.getDestination()==Destination.South):
                if (self.canTakeMore(self.North.lanePos3)):
                    self.North.lanePos3.add(self.East.lanePos1.pop())
                else: break
                firstVehicle = self.East.lanePos1.getFirst()

            #West lanes
            #cars making right turn to make u-turn
            firstVehicle = self.West.lanePos1.getFirst()
            while (firstVehicle.isSelfDriven()==VehcileType.Self_Driven and firstVehicle.getDestination()==Destination.North):
                if (self.canTakeMore(self.South.lanePos3)):
                    self.South.lanePos3.add(self.West.lanePos1.pop())
                else: break
                firstVehicle = self.West.lanePos1.getFirst()
        '''
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
