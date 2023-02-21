import torch
import cv2
import numpy  as np



class Detector:
    
    model = torch.hub.load('yolov5', 'yolov5n', source='local') 
    model.cuda()
        
    def detect(self,img):
        if img is not None:
            img = cv2.resize(img,(1000,650))
            result = self.model(img)

            df = result.pandas().xyxy[0]
          
            for ind in df.index:
                x1, y1 = int(df['xmin'][ind]), int(df['ymin'][ind])
                x2, y2 = int(df['xmax'][ind]), int(df['ymax'][ind])
                label = df['name'][ind]
                conf = df['confidence'][ind]
                text = label + ' ' + str(conf.round(decimals=2))
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.putText(img, "Current vehicle count"+str(len(df.index)), (15, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                cv2.putText(img, text, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
       
            return img , len(df.index)
        return np.zeros((1000,650)), 0 