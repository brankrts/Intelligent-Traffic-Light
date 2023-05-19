from flask import Flask,render_template,Response
import cv2
from CaptureVideos import Capturing
queue = None
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("home_page.html",queue = queue)

def generate_frames(path):
    capture = cv2.VideoCapture(path)
    while True:
        ret , frame = capture.read()
        ret , buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cv2.waitKey(1)
        
@app.route('/video_feed/<path>',methods = ['GET','POST'])
def video_feed(path):
    return Response(generate_frames(path), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    trafficManager = Capturing()
    queue = trafficManager.getQueue()
    app.run()
    trafficManager.start()
    
    while True :
        queue = trafficManager.getQueue()
    