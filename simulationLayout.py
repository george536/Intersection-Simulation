from random import randint
maxNumber=5
class Car:
    #def __init__(self,Type, source, destination, x, y):
    def __init__(self,Type, source, destination):
        self.Type=Type
        self.source=source
        self.destination=destination
        #self.x=x
        #self.y=y

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


class Lanes:
    global maxNumber
    def __init__(self):
        #pos means positive lane, cars are entering the intersection and exiting the lane (this is the right side of the road)
        self.lanePos1=[]
        self.lanePos2=[]
        self.lanePos3=[]
        #neg means negative lane, cars are exiting the intersection and entering the lane (this is the left side of the road)
        self.laneneg1=[]
        self.laneneg2=[]
        self.laneneg3=[]

    def addCar(self,vehicle):
        if(vehicle.getSource()==1):
            if(len(self.lanePos1)<=maxNumber):
                self.lanePos1.append(vehicle)
        if(vehicle.getSource()==2):
            if(len(self.lanePos2)<=maxNumber):
                self.lanePos2.append(vehicle)
        if(vehicle.getSource()==3):
            if(len(self.lanePos3)<=maxNumber):
                self.lanePos3.append(vehicle)

    
class Intersection:
    def __init__(self):
        self.rightDirection=Lanes()
        self.leftDirection=Lanes()
        self.topDirection=Lanes()
        self.bottomDirection=Lanes()

    def randomGenerater(self):
        #randomly select where the car is coming from
        origion=randint(1,4)
        #randomly select where the car is going
        destination=randint(1,3)
        #randomly select type of car
        temp=randint(1,2)
        if(temp==1):Type=False 
        else: Type=True

        
        if(origion==1):
            self.rightDirection.addCar(Car(Type,origion,destination))
        if(origion==2):
            self.topDirection.addCar(Car(Type,origion,destination))
        if(origion==3):
            self.leftDirection.addCar(Car(Type,origion,destination))
        if(origion==4):
            self.bottomDirection.addCar(Car(Type,origion,destination))


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

def main():
    design =Intersection()
    i=0
    while(i<5):
        design.randomGenerater()
        i+=1

    for i in range(0,4):
        for lane in design.rightLane:
            for car in lane
main()
