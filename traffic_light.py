import time 
from colors import RED,GREEN,YELLOW
class TrafficLight:
    
    def __init__(self,name,port = 1234):
        self.name = name
        self.density =5
        self.port = port
        self.count=0
        self.colorState = False
        self.light_color = RED
    def setDensity(self,density):
        self.density = density
        
    def getDensity(self):
        return self.density
    
    def toRed(self):
        print(self.name + " red is active") 
        self.light_color= RED
        self.colorState = False
        
    def toGreen(self):
        print(self.name +" green is active and density is " + str(self.getDensity()))
        self.colorState = True 
        self.count = self.getDensity()
        self.light_color= GREEN
        time.sleep(self.density * 1)
        self.count = 3 
        self.toYellow()
        time.sleep(3)
        self.toRed()
        
    def toYellow(self):
        print(self.name + " Yellow is active")
        self.light_color = YELLOW
    
        
    def getName(self):
        return self.name 
    
    def getCount(self):
        return self.count
    
    def setCount(self,count):
        self.count -= count
   
    def getColorState(self):
        return self.colorState