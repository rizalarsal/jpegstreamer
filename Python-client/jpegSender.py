import numpy as np
import cv2 as cv
import requests
import base64
import time

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imshow('Camera', frame)
    imencoded = cv.imencode(".jpg", frame)[1]
    dat= base64.b64encode(imencoded)
    p = len(dat)
    headers = {'Content-Type': 'image/jpeg', 'Content-Lenght':str(p)}
    response = requests.post("http://localhost:8000/upload",data=dat,headers=headers)
    print(response.text)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()