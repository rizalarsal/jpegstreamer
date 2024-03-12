import numpy as np
import cv2 as cv
import requests
import time
import traceback


extraTime =0.3
face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
lastTime= (time.time())  
while True:
    if lastTime < (time.time()+extraTime):
        lastTime= (time.time())+extraTime    
        try :
            response = requests.get("http://localhost:8000/view");
            if response.status_code == 200:
                frame = np.asarray(bytearray(response.content),dtype=("uint8"))
                frame = cv.imdecode(frame,cv.IMREAD_COLOR)
                gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
                for (x, y, w, h) in faces:
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cv.imshow('JPEG Viewer',frame)
            else :
                print("fail get response "+response.status_code);
        except Exception :
            traceback.print_exc()       
        if cv.waitKey(1) == ord('q'):
            break

cv.destroyAllWindows()



