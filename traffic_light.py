import time 
from colors import RED,GREEN,YELLOW
import threading
class TrafficLight:
    
    def __init__(self,name,port):
        self.name = name
        self.density = 1
        self.port = port
        self.light_color = (0,0,255)
    def setDensity(self,density):
        self.density = density
    def getDensity(self):
        return self.density
    def toRed(self):
        print(self.name + " red is active") 
        self.light_color= RED
        
    def toGreen(self):
        print(self.name +" green is active and density is " + str(self.getDensity())) 
        self.light_color= GREEN
        time.sleep(self.density * 2) 
        self.toRed()
        
    def toYellow(self):
        time.sleep(1)
        self.light_color = YELLOW
        time.sleep(1)
    def getName(self):
        return self.name 