import cv2 
from detector import Detector
import time



def local_video (path):
    cap = cv2.VideoCapture(path)
    prev_frame_time = 0
    new_frame_time = 0
    
    while(True):
        ret, frame = cap.read()   
        new_frame_time = time.time()
        if ret:
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            frame =  cv2.resize(frame, (600,600), interpolation=cv2.INTER_LINEAR)
            frame , total_waiting_time= Detector().detect(frame)
            fps = str(int(fps))
            fps = "FPS : " + fps
            time_to_wait = 'Wait: ' +str(total_waiting_time)
            cv2.putText(frame, fps, (300, 350), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 3)
            cv2.putText(frame, time_to_wait, (400, 500), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 3)
            cv2.imshow('Frame',frame)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    
local_video("assets/video2.mp4")