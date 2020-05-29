# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue, Pipe
import time
import sys
import pygame
from pygame.locals import *
from pygame.display import *

from random import *
import math
import cv2
import numpy as np
import funcVirus
import funcFirework
import funcDrawing
'''
mode
0 == SLEEP_MODE
1 == SELECT_MODE

10 == FIREWORK

20 == VIRUS

'''
BLACK= (0,0,0) #R G B
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255,180,0)
YELLOW = (255,255,0)
YELLOW_A = (255,255,0, 80)
PINK = (255,0, 255)
WHITE = (255,255,255)

sleep_img = pygame.image.load('SLEEP.png')

global W
W= 640
global H
H= 480

global innerW
innerW= 440
global innerH
innerH= int(380)



def gameScreen(StoU,recvXY):
    
    screen = pygame.display.set_mode((W,H), DOUBLEBUF )
    pygame.init()
    pygame.mixer.init()
    TARGET_FPS = 60
    clock = pygame.time.Clock()
    COUNT = 0
    SELECT_TIME = 10
    WARNING_TIME = 2
    PLAY_TIME = 10
    REWARD_TIME = 5
    fontObj = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 32)
    fontObjBig = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 70)  


    runned = False
    thresh_done=False
    center = (0,0)
    mode = 0
    cam_on = False
    select_start = False
    warning_start = False
    play_start = False
    reward_start = False
    winner_mode = 0

    virus_winners = [0,0,0]
    firework_winners = [0,0,0]
    reward_winners = [0,0,0]

    frontcam = cv2.VideoCapture(0)
    frontcam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    frontcam.set(cv2.CAP_PROP_FRAME_WIDTH,W)
    frontcam.set(cv2.CAP_PROP_FRAME_HEIGHT,H)
    ret, frame = frontcam.read()

    background_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    background_img = cv2.GaussianBlur(background_img, (5,5),255)
    sleep_start_time = time.time()
    cam_on = True
    
    while True:
        COUNT +=1
        screen.fill(BLACK)
        
        if recvXY.poll():
            center = recvXY.recv()
                

        if mode == 0:
            screen.blit(sleep_img,(0,0))
##            if cam_on :
##                ret, frame = frontcam.read() #배경캡쳐 됨
##                cv2.imshow("screen",frame)
            
            if cam_on == True and int(time.time() - sleep_start_time) > 30:
                frontcam.release()
                print("relased")
                cam_on = False

            
        elif mode == 1:
            
            select_limit_time = SELECT_TIME -int(time.time()-select_start_time)
            if select_limit_time < 0:
                if center[0] <int((W-innerW)/2)+innerW/3:
                    textSurfaceObj = fontObjBig.render("Let's start FIREWORK", True, WHITE)
                    screen.blit(textSurfaceObj, (10,70))

                    firework = funcFirework.FireFunc(screen)
                    mode = 10 # [ FIREWORK ]
                    winner_mode = 10
                    
                elif center[0] <int((W-innerW)/2)+innerW/3*2:
                    textSurfaceObj = fontObjBig.render("Let's start DRAWING", True, WHITE)
                    screen.blit(textSurfaceObj, (10,70))

                    drawing = funcDrawing.Drawing(screen)
                    mode = 30 # [ DRAWING ]
                    winner_mode = 30
                    
                else:                    
                    textSurfaceObj = fontObjBig.render("Let's start VIRUS", True, WHITE)
                    screen.blit(textSurfaceObj, (50,70))

##                    virus = funcVirus.VirusFunc(screen)
##                    mode = 20 # [ VIRUS ]
##                    winner_mode = 20
                    firework = funcFirework.FireFunc(screen)
                    mode = 10 # [ FIREWORK ]
                    winner_mode = 10
                
                pygame.display.flip()  # 화면 전체를 업데이트
                clock.tick(TARGET_FPS)
                cv2.waitKey(1000)
                screen.fill(BLACK)
                play_start_time = time.time()
                play_start = True

            else:
                textSurfaceObj = fontObj.render("SELECT TIME:"+str(select_limit_time), True, GREEN)
                screen.blit(textSurfaceObj, (10,10))
                
                pygame.draw.rect(screen, RED, [int((W-innerW)/2), H-innerH,innerW/3, H],2) #x,y,w,h [FIREWORK]
                pygame.draw.rect(screen, PINK, [int((W-innerW)/2)+innerW/3, H-innerH, innerW/3, H],2) # [DRAWING]
                pygame.draw.rect(screen, GREEN, [int((W-innerW)/2)+innerW/3*2, H-innerH, innerW/3, H],2) # [VIRUS]
            
                if center[0] <int((W-innerW)/2)+innerW/3:
                    pygame.draw.rect(screen, WHITE, [int((W-innerW)/2), H-innerH,innerW/3, H],5) #x,y,w,h [FIREWORK]
                    
                elif int((W-innerW)/2)+innerW/3 <= center[0] <int((W-innerW)/2)+innerW/3*2:
                    pygame.draw.rect(screen, WHITE, [int((W-innerW)/2)+innerW/3, H-innerH, innerW/3, H],5) # [DRAWING]
                elif int((W-innerW)/2)+innerW/3*2 <= center[0] < int((W-innerW)/2)+innerW:
                    pygame.draw.rect(screen, WHITE, [int((W-innerW)/2)+innerW/3*2, H-innerH, innerW/3, H],5) # [VIRUS]
                    
                pygame.draw.circle(screen, (255,255,255), center,15,0)
                
            if cam_on :
                ret, frame = frontcam.read() #배경캡쳐 됨
                cv2.imshow("screen",frame)
                
        elif mode == 2:
            reward_limit_time = REWARD_TIME -int(time.time()-reward_start_time)
            if reward_limit_time < 0:
                reward_start = False
                select_start = False

            else:
                if winner_mode == 10:
                    textSurfaceObj = fontObj.render("FIRE REWARD TIME:"+str(reward_limit_time), True, GREEN)
                    screen.blit(textSurfaceObj, (10,400))
                    
                elif winner_mode == 20:
                    textSurfaceObj = fontObj.render("VIRUS REWARD TIME:"+str(reward_limit_time), True, GREEN)
                    screen.blit(textSurfaceObj, (10,400))

                elif winner_mode == 30:
                    textSurfaceObj = fontObj.render("DRAWING REWARD TIME:"+str(reward_limit_time), True, GREEN)
                    screen.blit(textSurfaceObj, (10,400))
                                        
                textSurfaceObj = fontObj.render("REWARD TIME:"+str(reward_limit_time), True, GREEN)
                screen.blit(textSurfaceObj, (10,440))
                
        else:   #[컨텐츠 실행 처리]
            play_limit_time = PLAY_TIME -int(time.time()-play_start_time)
            ret, frame = frontcam.read()
            
            if play_limit_time < 0: #리워드로 넘어가야됨 -----> 수정) Play_start == False
                play_start = False
                mode = 2
                reward_start_time = time.time()

                if winner_mode == 1:
                    my_person_img = upload_img('./firework_imgs/output/popimage.jpg') ##
                    my_screen_img = pygame.image.load('./firework_imgs/output/screenshot.jpg')
                    my_qr_img = pygame.image.load('./firework_imgs/output/qr_popimage.jpg')
                    score1_img = pygame.image.load('./firework_imgs/output/score1.jpg')
    
                    my_person_img = pygame.transform.scale(my_person_img, (int(W/4), int(H/4)))
                    my_qr_img = pygame.transform.scale(my_qr_img, (int(W/4), int(H/4)))
                    my_screen_img = pygame.transform.scale(my_screen_img, (int(W/4), int(H/4)))
                    score1_img = pygame.transform.scale(score1_img, (int(W/4), int(H/4)))
                    
                    text1 = fontObj.render("1 st: " + str(reward_winners[0]),20,(0,128,0))
                    screen.blit(text1,(10,120))
                    text2 = fontObj.render("2 nd: " + str(reward_winners[1]),20,(0,128,0))
                    screen.blit(text2,(10,140))
                    text3 = fontObj.render("3 rd: " + str(reward_winners[2]),20,(0,128,0))
                    screen.blit(text3,(10,160))

                    screen.blit(score1_img, (0,0)) # 1등 사진
                    screen.blit(my_screen_img, (5,H/2))
                    screen.blit(my_qr_img, (W/2-W/8, H/2))
                    screen.blit(my_person_img, (W-W/4-5, H/2))
                    
                elif winner_mode == 2:
                    my_person_img = upload_img('./virus_imgs/output/popimage.jpg') ##
                    my_screen_img = pygame.image.load('./virus_imgs/output/screenshot.jpg')
                    my_qr_img = pygame.image.load('./virus_imgs/output/qr_popimage.jpg')
                    score1_img = pygame.image.load('./virus_imgs/output/score1.jpg')
    
                    my_person_img = pygame.transform.scale(my_person_img, (int(W/4), int(H/4)))
                    my_qr_img = pygame.transform.scale(my_qr_img, (int(W/4), int(H/4)))
                    my_screen_img = pygame.transform.scale(my_screen_img, (int(W/4), int(H/4)))
                    score1_img = pygame.transform.scale(score1_img, (int(W/4), int(H/4)))
                    
                    text1 = fontObj.render("1 st: " + str(reward_winners[0]),20,(0,128,0))
                    screen.blit(text1,(10,120))
                    text2 = fontObj.render("2 nd: " + str(reward_winners[1]),20,(0,128,0))
                    screen.blit(text2,(10,140))
                    text3 = fontObj.render("3 rd: " + str(reward_winners[2]),20,(0,128,0))
                    screen.blit(text3,(10,160))

                    screen.blit(score1_img, (0,0)) # 1등 사진
                    screen.blit(my_screen_img, (5,H/2))
                    screen.blit(my_qr_img, (W/2-W/8, H/2))
                    screen.blit(my_person_img, (W-W/4-5, H/2))
                
                
            else:
                textSurfaceObj = fontObj.render("PLAY TIME:"+str(play_limit_time), True, GREEN)
                screen.blit(textSurfaceObj, (100,10))
                if mode == 10:
                    if ret:
                        firework.fireMain(background_img, frame)

                elif mode == 20:
                    if ret:
                        virus.virusMain(background_img, frame)
                        
                elif mode == 30: #발자국 찍기
                    if ret:
                        drawing.drawingMain(center,frame) 
                    textSurfaceObj = fontObj.render("Do DRAWING", True, GREEN)
                    screen.blit(textSurfaceObj, (10,50))
                        
                        
       
        if StoU.poll():
            RECV_MODE = StoU.recv()
            
            if RECV_MODE == "SLEEP_MODE":
                select_start = False
                if cam_on == True:
                    sleep_start_time = time.time()
                    mode = 0
                
            elif RECV_MODE == "SELECT_MODE":
                if select_start == False : #셀렉트 타임아웃때문에 필요한 select_time
                    select_start = True
                    select_start_time = time.time()
                    
                    if cam_on ==False:
                        screen.fill(BLACK)
                        textSurfaceObj = fontObj.render("LOADING", True, WHITE)
                        screen.blit(textSurfaceObj, (210,H/2))
                        pygame.display.flip()  # 화면 전체를 업데이트
                                
                        frontcam = cv2.VideoCapture(0)
                        frontcam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
                        frontcam.set(cv2.CAP_PROP_FRAME_WIDTH,W)
                        frontcam.set(cv2.CAP_PROP_FRAME_HEIGHT,H)
                        
                        cam_on = True
                        mode = 1

                    elif cam_on ==True:
                        mode = 1
                        
            elif RECV_MODE == "ONE_PERSON_WARNING":
##                textSurfaceObj = fontObj.render("Just ONE Person", True, RED, WHITE)
##                screen.blit(textSurfaceObj, (210,400))
                warning_start = True
                warning_start_time = time.time()
                
                ##else: ## 처리해야되나 !?!?!?
##        if warning_start == True:
##            warning_limit_time = WARNING_TIME -int(time.time()-warning_start_time)
##            if warning_limit_time > 0:
##                textSurfaceObj = fontObj.render("Just ONE Person", True, RED, WHITE)
##                screen.blit(textSurfaceObj, (210,400))
##            else:
##                warning_start = False
                    
                
        pygame.display.flip()  # 화면 전체를 업데이트
        clock.tick(TARGET_FPS)  # 프레임 수 맞추기
        
        cv2.waitKey(1)

##        
##UtoS, StoU = Pipe()
##sendXY, recvXY = Pipe()
##UtoS.send("SELECT_MODE")
##sendXY.send((320,240))
##gameScreen(StoU,recvXY)
