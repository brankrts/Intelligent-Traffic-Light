from torch.hub import load
import cv2
import numpy  as np
from const_model import RoiModel
from constants import TRUCK_WAITING_TIME,CAR_WAITING_TIME,MOTORCYCLE_WAITING_TIME,BUS_WAITING_TIME,TRUCK,CAR,MOTORCYCLE,BUS,ROI1,ROI2,ROI3
from colors import RED,GREEN,BLUE
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Detector:
    
    model = load('yolov5', 'yolov5l', source='local') 
    model.cuda()
    labels = ["car","truck","bus","motorcycle"]
    radius= 4
    lineType = 8
    circleThickness = -1
    lineThickness = 2
    
    def __init__(self):
        self.roi1 = RoiModel(ROI1)
        self.roi2 = RoiModel(ROI2)
        self.roi3 = RoiModel(ROI3)
        
    def detect(self,img):
        
        current_values = None
        current_values =dict(
     
            roi1 = {
                'truck' : 0,
                'car' : 0,
                'bus' : 0,
                'motorcycle' : 0,
                'total_waiting_time' : 0
            },
            roi2 = {
                'truck' : 0,
                'car' : 0,
                'bus' : 0,
                'motorcycle' : 0,
                'total_waiting_time' : 0
            },
            roi3 = {
                'truck' : 0,
                'car' : 0,
                'bus' : 0,
                'motorcycle' : 0,
                'total_waiting_time' : 0
            }
        )
        
        
       
        if img is not None:
            
            #img = cv2.resize(img,(1000,650))
            result = self.model(img)
            
            self.drawRoiCircles(img,self.roi1)
            self.drawRoiCircles(img,self.roi2)
            self.drawRoiCircles(img,self.roi3)

            df = result.pandas().xyxy[0]
            
            for ind in df.index:
                x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
                x2, y2 = int(df['xmax'][ind]), int(df['ymax'][ind])
                label = df['name'][ind]
                #conf = df['confidence'][ind]
    
                if label in self.labels:
                    center_x = x1 + int((x2-x1)/2)
                    center_y = y1 + int((y2-y1)/2)
                   
                    self.calculateDensityForArea(img,label,center_x,center_y,self.roi1,current_values) 
                    self.calculateDensityForArea(img,label,center_x,center_y,self.roi2,current_values) 
                    self.calculateDensityForArea(img,label,center_x,center_y,self.roi3,current_values) 
                    
                  #toplam 3 e bolunecek ( serit sayisi) 
            return img , max(current_values[self.roi1.name]["total_waiting_time"],current_values[self.roi2.name]["total_waiting_time"],current_values[self.roi3.name]["total_waiting_time"])
        return np.zeros((1000,650)), 0 
    
    def findVehicleType(self,label):
        if label == TRUCK:
            return TRUCK_WAITING_TIME
        if label == CAR:
            return CAR_WAITING_TIME
        if label == BUS:
            return BUS_WAITING_TIME
        if label == MOTORCYCLE:
            return MOTORCYCLE_WAITING_TIME
    
    # def findROIArea(self,centerX,centerY):
        #currentRoi = ""
        #roi1 = ROI1["x1"] -50 < centerX and ROI1["y1"] < centerY and ROI1["x2"] > centerX and ROI1["y2"] < centerY and ROI1["x3"] > centerX and ROI1["y3"] > centerY and ROI1["x4"] < centerX and ROI1["y4"] > centerY
        # roi2 = ROI2["x1"] < centerX and ROI2["y1"] < centerY and ROI2["x2"] + 50 > centerX and ROI2["y2"] < centerY and ROI2["x3"] > centerX and ROI2["y3"] > centerY and ROI2["x4"] < centerX and ROI2["y4"] > centerY
        #roi3 = ROI3["x1"] -50 < centerX and ROI3["y1"] < centerY and ROI3["x2"] > centerX and ROI3["y2"] < centerY and ROI3["x3"] > centerX and ROI1["y3"] > centerY and ROI3["x4"] < centerX and ROI3["y4"] > centerY

        # if roi1:
        #    currentRoi = "ROI1"
        # if roi2:
        #    currentRoi = "ROI2"
        #if roi3:
           # currentRoi = "ROI3"
            
        #return  currentRoi
    
    def drawVehicleCenterCoords(self,image,centerx,centery):
        
        image = cv2.circle(image, (centerx,centery), self.radius,color = RED , thickness=self.circleThickness)
        
        return image
    
    def drawRoiCircles(self,image,roi):
        
        corner_points = [(roi.x1,roi.y1),(roi.x2,roi.y2),(roi.x3,roi.y3),(roi.x4,roi.y4)]
        for corner in corner_points:
            image = cv2.circle(image, corner, self.radius,color = BLUE , thickness=self.circleThickness)
            
        
        cv2.line(image, corner_points[0],corner_points[1], GREEN, thickness=self.lineThickness, lineType=self.lineType)
        cv2.line(image, corner_points[0],corner_points[3], GREEN, thickness=self.lineThickness, lineType=self.lineType)
        cv2.line(image, corner_points[1],corner_points[2], GREEN, thickness=self.lineThickness, lineType=self.lineType)
        cv2.line(image, corner_points[2],corner_points[3], GREEN, thickness=self.lineThickness, lineType=self.lineType)
        
        
        return image
        
    def isInArea(self,centerx,centery,roi):
        polygon = Polygon([(roi.x1,roi.y1), (roi.x2,roi.y2), (roi.x3,roi.y3), (roi.x4,roi.y4)])
        point = Point(centerx,centery)
        
        return polygon.contains(point)
        
    def  calculateDensityForArea(self,img,label,center_x,center_y,roi,current_values):
        
       if self.isInArea(center_x,center_y,roi):
            img = self.drawVehicleCenterCoords(img,center_x,center_y)
            current_values[roi.name][label] += 1 
            current_values[roi.name]['total_waiting_time'] += current_values[roi.name][label] * self.findVehicleType(label)
