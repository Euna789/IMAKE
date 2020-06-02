import cv2
import numpy as np

def preprocess(frame):

    frame = cv2.bilateralFilter(frame, 9, 75, 75)

    ret, frame = cv2.threshold(frame, 30, 255, cv2.THRESH_BINARY_INV)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)

    frame[:,:,0] = cv2.equalizeHist(frame[:,:,0])

    aft_hist = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)

    frame = cv2.cvtColor(aft_hist, cv2.COLOR_BGR2GRAY)

    ret, frame = cv2.threshold(frame, 14, 255, cv2.THRESH_BINARY_INV)
    
    return frame

def detect(frame):
    
global W
W= 640
global H
H= 480

cap = cv2.VideoCapture("7.mp4")
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,H)

# 비디오 읽어와서 hough detect 실행

while True:
    _, frame = cap.read()

    
    frame = cv2.resize(frame, (640,480))
    
    orig_frame = frame
    cv2.imshow('original', frame)    
    cv2.waitKey(1)

    frame = preprocess(frame)
    
    frame = cv2.Canny(frame, 20, 100)

    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1.12, minDist = 80,\
                               param1=50, param2 = 30, minRadius = 0, maxRadius = 70)
    if circles is not None:
        for c in circles [0,:]:
            center = (c[0],c[1])
            radius = c[2]
            cv2.circle(orig_frame, center, radius, (0,255,0),2)
            cv2.circle(orig_frame, center, 2, (0,255,0),2)
            
    cv2.imshow("realtime", orig_frame)
    cv2.waitKey(1)

    

