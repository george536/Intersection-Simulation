class Car:
    def __init__(self,Type, source, destination, x, y):
        self.Type=Type
        self.source=source
        self.destination=destination
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
        return self.getDestination


class Lanes:
    def __init__(self):
        self.lanePos1=[]
        self.lanePos2=[]
        self.lanePos3=[]
        self.laneneg1=[]
        self.laneneg2=[]
        self.laneneg3=[]
    
class Intersection:
    def __init__(self):
        self.rightLane=Lanes()
        self.leftLane=Lanes()
        self.topLane=Lanes()
        self.bottomLane=Lanes()


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
    intersection1=Intersection()
    
main()
