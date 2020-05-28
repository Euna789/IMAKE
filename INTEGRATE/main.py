from threading import Thread
import cv2
from multiprocessing import Process, Queue, Pipe
from uppercamera import *
from tempscreen import *
from piptest import *

def f():
    video = cv2.VideoCapture('video2.mp4')
    while True:
        ret, orig_frame = video.read()
        if not ret:
            video = cv2.VideoCapture('video2.mp4')
            continue
        orig_frame = cv2.resize(orig_frame, (640,480))
        cv2.imshow("frame", orig_frame)
        cv2.waitKey(10)
     
if __name__ == '__main__':
    UtoS, StoU = Pipe()
    sendXY, recvXY = Pipe()
    uppercam_pr = Process(target=upperCam, args=(UtoS,sendXY))
    gamescreen_pr = Process(target=gameScreen, args=(StoU,recvXY))
 
    uppercam_pr.start()
    gamescreen_pr.start()


