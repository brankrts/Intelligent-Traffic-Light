import cv2
from object_detector import Detector
from Queue import LightQueue
from traffic_light import TrafficLight
from multiprocessing import Process


class Capturing:
    
    def __init__(self):
        self.detector = Detector()
        self.light1 = TrafficLight(name="light1") 
        self.light2 = TrafficLight(name="light2")
        self.light3 = TrafficLight(name="light3")
        self.light4 = TrafficLight(name="light4")
        self.queue = LightQueue()
        self.queue.push(self.light1)
        self.queue.push(self.light2)
        self.queue.push(self.light3)
        self.queue.push(self.light4)
 
        
    def start(self):
        p1 = Process(target=self.local_video, args=(self.queue,"video1.mp4",self.light1),daemon=True)
        p2 = Process(target=self.local_video, args=(self.queue,"video2.mp4",self.light2),daemon=True)
        p3 = Process(target=self.local_video, args=(self.queue,"video3.mp4",self.light3),daemon=True)
        p4 = Process(target=self.local_video, args=(self.queue,"video4.mp4",self.light4),daemon=True)
        p5 =Process(target=self.lightChanges, args=(self.queue,))
        
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start() 
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()

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


    def local_video(self,queue,path,light):
        cap = cv2.VideoCapture(path)
        while(True):
            ret, frame = cap.read()   
                
            if ret:
                frame , density= self.detector.detect(frame)
                light.setDensity(density)
                frame = self.resizeImage(frame)
                queue.updateLight(light,density)
                cv2.imshow(light.name, frame)
                if cv2.waitKey(2) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()


    def resizeImage(self,image):
        down_width = 400
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


