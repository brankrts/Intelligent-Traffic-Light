import cv2
import time
import math
import numpy as np
from line_count_finder import LineCountFinder
from contour_finder import LineContourFinder
from roi_filter import ROIFilter
from detector import Detector
from constants import MAIN_ROI
from colors import RED, GREEN
from thread_pool import ThreadPool
from traffic_light import TrafficLight
from threading import Thread
from custom_queue import Queue


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
        ver_con = np.concatenate(hor)

    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        ver = hor
    return ver


class CaptureVideos:

    def __init__(self):
        self.thread_pool = ThreadPool()
        self.light1 = TrafficLight(name="light1")
        self.light2 = TrafficLight(name="light2")
        self.light3 = TrafficLight(name="light3")
        self.light4 = TrafficLight(name="light4")
        self.queue = Queue([self.light1,self.light2,self.light3,self.light4])
        self.total_density = sum([self.light1.get_current_density(), self.light2.get_current_density(
        ), self.light3.get_current_density(), self.light4.get_current_density()])
        self.cams = {
            "light1" : np.zeros((400,400),dtype=np.uint8),
            "light2" : np.zeros((400,400) , dtype=np.uint8),
            "light3" : np.zeros((400,400),dtype=np.uint8),
            "light4" : np.zeros((400,400) , dtype=np.uint8),
        }
    def local_video(self, path, light: TrafficLight,index):

        cap = cv2.VideoCapture(path)
        prev_frame_time = 0
        new_frame_time = 0
        finder = LineContourFinder(contour_threshold=200,
                                   contour_distance=0, contour_area_threshold=50)
        lane_count = None
        
        ret, frame = cap.read() 
      
        frame, window_size = ROIFilter().getFilteredImage(frame, MAIN_ROI)
        contour_model = finder.get_all_values(window_size)
        count_finder = LineCountFinder(
            contour_model=contour_model, min_y_threshold=5, max_y_threshold=50)

        lane_count, model = count_finder.visualize()

        stacked_image = stackImages([model.original_image, model.binary_image, model.max_area_mask,
                                    model.contour_img, model.line_image, model.contour_in_max_contour_area_image], 1)

        stacked_image = cv2.resize(stacked_image, (300, 300))
         
        while(True):

            current_density = 0
            ret, frame = cap.read()
            new_frame_time = time.time()
            
            if ret:
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                frame, total_waiting_time, current_density = Detector().detect(frame)

                light.set_current_density(current_density)
                light.set_green_time(total_waiting_time)
                light.set_overall_vehicle_density(self.total_density)
                light.set_priority()
                
                frame =  cv2.circle(frame,(120,500),50,light.light_color,-1)
                

                frame = cv2.resize(frame, (400, 400))
                fps = "FPS : " + str(int(fps))
                time_to_wait = 'Green Time: ' + \
                    str(int(total_waiting_time/lane_count))
                lines = "Lane Count : " + str(lane_count)
                cv2.putText(frame, fps, (10, 40),
                            cv2.FONT_HERSHEY_PLAIN, 2, RED, 3)
                cv2.putText(frame, time_to_wait, (10, 80),
                            cv2.FONT_HERSHEY_PLAIN, 2, GREEN, 3)
                cv2.putText(frame, lines, (10, 120),
                            cv2.FONT_HERSHEY_PLAIN, 2, GREEN, 3)
                self.cams[light.name] = frame
                

    def join_cams(self):
        
            while True:
                
                stacked_image = stackImages([[self.cams["light1"],self.cams["light2"],self.cams["light3"],self.cams["light4"]]],1)
                stacked_image = cv2.resize(stacked_image, (1700, 500))
                cv2.imshow("Kavsaklar", stacked_image)
                if cv2.waitKey(12) & 0xFF == ord('q'):
                    break
            
    def start(self):

        self.thread_pool.add_thread(Thread(target=self.local_video, args=(
            "assets/video2.mp4", self.light1, 0), daemon=True))
        self.thread_pool.add_thread(Thread(target=self.local_video, args=(
            "assets/video2.mp4", self.light2, 1), daemon=True))
        self.thread_pool.add_thread(Thread(target=self.local_video, args=(
            "assets/video2.mp4", self.light3, 2), daemon=True))
        self.thread_pool.add_thread(Thread(target=self.local_video, args=(
            "assets/video2.mp4", self.light4, 3), daemon=True))
        self.thread_pool.add_thread(Thread(target=self.light_changes, args=(self.queue,)))
        
        self.thread_pool.add_thread(Thread(target=self.join_cams))

        self.thread_pool.start_threading()

    def light_changes(self, queue : Queue):
        
         while True:
             
            light : TrafficLight = queue.pop()
            
            print(f"{light.name} trafik isigi yesil kalma suresi : {light.get_green_time()}\n")
            
            light.to_green()
            queue.push(light)
            queue.update_priority()
            
            max_priority = max(queue.queue,key=lambda light:light.priority)
            for light in self.queue.queue:
                print(f'{light.getName()} --> Oncelik degeri : {light.get_priority()/max_priority.priority:.6f}')
            print("\n")
        

if __name__ == "__main__":

    capturing = CaptureVideos()
    capturing.start()
