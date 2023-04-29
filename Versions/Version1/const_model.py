import numpy as np

class RoiModel:
     
    def __init__(self,roi):
        
        self.name = roi["name"]
        self.x1 = roi["x1"]
        self.y1 = roi["y1"]
        self.x2 = roi["x2"]
        self.y2 = roi["y2"]
        self.x3 = roi["x3"]
        self.y3 = roi["y3"]
        self.x4 = roi["x4"]
        self.y4 = roi["y4"]
        
        self.window_x = roi["window_sizes"]["x"]
        self.window_y = roi["window_sizes"]["y"]
        self.window_width = roi["window_sizes"]["width"]
        self.window_height = roi["window_sizes"]["height"]
        
    def getRoiCorners(self):
        return np.array([[(self.x1,self.y1), (self.x2,self.y2), (self.x3,self.y3),(self.x4,self.y4)]], dtype=np.int32)
    
    def getWindowSize(self,image):
        return image[self.window_y:self.window_y+self.window_height,self.window_x:self.window_x+self.window_width]
        