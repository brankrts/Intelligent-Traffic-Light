import cv2
import threading
from object_detector import Detector
from Queue import LightQueue
from multiprocessing import Process
from traffic_light import TrafficLight
from thread_pool import ThreadPool
from connection import Connection
import time


class Capturing:
    
    def __init__(self):
        self.detector = Detector()
        self.light1 = TrafficLight(name="light1") 
        self.light2 = TrafficLight(name="light2")
        self.light3 = TrafficLight(name="light3")
        self.light4 = TrafficLight(name="light4")
        self.tempLight= None
        self.tempDensity = None
        self.queue = LightQueue()
        self.queue.push(self.light1)
        self.queue.push(self.light2)
        self.queue.push(self.light3)
        self.queue.push(self.light4)
 
        
    def start(self):
   
        thread_pool = ThreadPool()
        thread_pool.add_thread(threading.Thread(target=self.local_video, args=("video1.mp4",self.light1),daemon=True))
        thread_pool.add_thread(threading.Thread(target=self.local_video, args=("video2.mp4",self.light2),daemon=True))
        thread_pool.add_thread(threading.Thread(target=self.local_video, args=("video3.mp4",self.light3),daemon=True))
        thread_pool.add_thread(threading.Thread(target=self.local_video, args=("video4.mp4",self.light4),daemon=True))
        thread_pool.add_thread(threading.Thread(target=self.lightChanges, args=(self.queue,)))
        thread_pool.start_threading()
        thread_pool.join_thread()
       
    def getQueue(self):
        return self.queue 

    def webcam_video(self):
        cap = cv2.VideoCapture(0)
        while(True):
            ret, frame = cap.read()
            if ret:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()


    def local_video (self,path,light):
        cap = cv2.VideoCapture(path)
        
        prev_frame_time = 0
        new_frame_time = 0
        while(True):
            ret, frame = cap.read()   
            new_frame_time = time.time()
            if ret:
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                frame , density= self.detector.detect(frame)
                frame =  cv2.circle(frame,(120,500),50,light.light_color,-1)
                light.setDensity(density)
                frame = self.resizeImage(frame)
                
                fps = str(int(fps))
                fps = "FPS : " + fps
                cv2.putText(frame, fps, (300, 350), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 3)
                cv2.imshow(light.name, frame)
                if cv2.waitKey(2) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    def from_unity(self,port,light):
        connection = Connection(port=port)
        conn , addr = connection.start_connection()
        while(True):
            image = connection.get_client_image(conn=conn)
            image , density = self.detector.detect(image)
            light.setDensity(density)
            image = self.resizeImage(image=image)
            cv2.imshow(light.name,image)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                connection.close_connection()
                cv2.destroyAllWindows()
                break 
        connection.close_connection()    
        cv2.destroyAllWindows()

    def resizeImage(self,image):
        down_width = 450
        down_height = 400
        down_points = (down_width, down_height)
        resized_down = cv2.resize(
        image, down_points, interpolation=cv2.INTER_LINEAR)
        return resized_down
        
    def lightChanges(self,queue):
        while True:
            light = queue.pop()
            light.toGreen()
            queue.push(light)
            


