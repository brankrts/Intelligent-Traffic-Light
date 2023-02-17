import time 
class TrafficLight:
    
    
    def __init__(self,name):
        self.name = name
        self.density = 1
    def setDensity(self,density):
        self.density = density
    def getDensity(self):
        return self.density
    def toRed(self):
        print(self.name + " red is active") 
        
    def toGreen(self):
        print(self.name +" green is active and density is " + str(self.getDensity())) 
    
        time.sleep(self.density * 2) 
        self.toRed()
    def getName(self):
        return self.name 