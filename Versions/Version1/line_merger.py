import cv2
import numpy as np

from sklearn.linear_model import LinearRegression


class LineMerger:
    
    def __init__(self, line_distance_threshold=30):
        self.line_distance_threshold = line_distance_threshold

    def detect(self, image,lines):
       
        groups = []
        for line in lines:
            x1, y1, x2, y2 = line
            added = False
            for group in groups:
                if added:
                    break
                for g_line in group:
                    g_x1, g_y1, g_x2, g_y2 = g_line
                    if (abs(x1 - g_x1) < 20 and abs(y1 - g_y1) < 20) or (abs(x2 - g_x2) < 20 and abs(y2 - g_y2) < 20):
                        group.append(line)
                        added = True
                        break
            if not added:
                groups.append([line])

        
        for group in groups:
           
            x1_list, y1_list, x2_list, y2_list = [], [], [], []
            for line in group:
                x1, y1, x2, y2 = line
                x1_list.append(x1)
                y1_list.append(y1)
                x2_list.append(x2)
                y2_list.append(y2)
            points = np.column_stack([x1_list + x2_list, y1_list + y2_list])
            model = LinearRegression().fit(points[:, 0].reshape(-1, 1), points[:, 1])
            slope, intercept = model.coef_[0], model.intercept_
            x1 = 0
            y1 = int(slope * x1 + intercept)
            x2 = image.shape[1]
            y2 = int(slope * x2 + intercept)
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), thickness=3)

        return image,len(groups)
    
