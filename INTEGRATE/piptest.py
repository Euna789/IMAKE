from threading import Thread
import cv2
from multiprocessing import Process, Queue, Pipe

def pipetest(UtoS):
    while True:
        UtoS.send(input())
