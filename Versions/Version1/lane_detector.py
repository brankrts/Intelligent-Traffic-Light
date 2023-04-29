import cv2
import numpy as np
from sklearn.linear_model import LinearRegression



class LaneDetector:
    
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path, 0)
        self.img = cv2.threshold(self.img, 127, 1, cv2.THRESH_BINARY)[1]
        self.points = np.column_stack(np.where(self.img == 1))

    def find_lane_lines(self):
        

        model = LinearRegression().fit(self.points[:, 0].reshape(-1, 1), self.points[:, 1])
        slope, intercept = model.coef_[0], model.intercept_


        lines = cv2.HoughLinesP(self.img, rho=1, theta=np.pi/180,
                                threshold=45, minLineLength=20, maxLineGap=10)
       
        coords = []
        
        for line in lines:
       
            x1, y1, x2, y2 = line[0]
            points = np.column_stack([[x1, x2], [y1, y2]])
            model = LinearRegression().fit(points[:, 0].reshape(-1, 1), points[:, 1])
            slope, intercept = model.coef_[0], model.intercept_
            x1 = 0
            y1 = int(slope * x1 + intercept)
            x2 = self.img.shape[1]
            y2 = int(slope * x2 + intercept)
            coords.append([x1,y1,x2,y2])
            

        return coords