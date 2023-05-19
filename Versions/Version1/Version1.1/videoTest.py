import cv2
import numpy as np

from line_count_finder import LineCountFinder
from contour_finder import LineContourFinder
from constants import MAIN_ROI2 , MAIN_ROI1 , MAIN_ROI3 , MAIN_ROI4
from roi_filter import ROIFilter,RoiModel

def stackImages(imgArray, scale):

        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2:
                        imgArray[x][y] = cv2.cvtColor(
                            imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
                hor_con[x] = np.concatenate(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                if len(imgArray[x].shape) == 2:
                    imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            hor_con = np.concatenate(imgArray)
            ver = hor
        return ver



path = "assets/video4.mp4"

const_model = RoiModel(MAIN_ROI4)

cap = cv2.VideoCapture(path)
prev_frame_time = 0
new_frame_time = 0
finder = LineContourFinder(contour_threshold=const_model.contour_threshold,
                                   contour_distance=const_model.contour_distance, contour_area_threshold=const_model.contour_area_threshold)
lane_count = None
        
ret, frame = cap.read() 


frame, window_size = ROIFilter().getFilteredImage(frame, MAIN_ROI4)
contour_model = finder.get_all_values(window_size)
count_finder = LineCountFinder(
contour_model=contour_model, min_y_threshold=const_model.min_y_threshold, max_y_threshold=const_model.max_y_threshold)

lane_count, model = count_finder.visualize()
frame = cv2.resize(frame , (400,400))
cv2.imshow("Binary" , model.binary_image)
cv2.waitKey(0)

stacked_image = stackImages([model.original_image, model.binary_image, model.max_area_mask,
                                    model.contour_img, model.line_image, model.contour_in_max_contour_area_image], 1)
stacked_image = cv2.resize(stacked_image, (1500, 500))

cv2.imshow("frame" , stacked_image)
cv2.waitKey(0)
 
