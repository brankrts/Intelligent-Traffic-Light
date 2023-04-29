import cv2


cap = cv2.VideoCapture("assets/video2.mp4")
x1 = 39
y1 = 210
x2 = 458
y2 = 202
x3 = 733
y3 = 603
x4 = 6
y4 = 603
while True :
    
    ret , frame = cap.read()
    
    if ret :
        roi = cv2.selectROI("Roi",frame)
        print(roi)
        cv2.imshow("frame" , frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()
