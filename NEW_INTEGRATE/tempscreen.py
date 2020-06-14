# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue, Pipe
import time
import sys
import pygame
from pygame.locals import *
from pygame.display import *
import img_upload
from random import *
import math
import cv2
import numpy as np
import funcVirus
import funcFirework
import funcDrawing
import dbManager 
'''
mode
0 == SLEEP_MODE
1 == SELECT_MODE

10 == FIREWORK

"DRAWING" == VIRUS!!

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

sleep_img = pygame.image.load('./ui_imgs/sleep.png')
blank = pygame.image.load('./ui_imgs/blank.png')

global playMusic, playReward, music, rewardMusic
pygame.mixer.init()
pygame.mixer.pre_init(44100,-16,2,512)
music = pygame.mixer.Sound('bgMusic.ogg')
playMusic = False
rewardMusic = pygame.mixer.Sound('reward.ogg')
playReward = False

global W
W= 640
global H
H= 480

global innerW
innerW=W #440
global innerH
innerH=H #380

def comparingScore(winner_array, my_score, my_img, where):
    winner_array.append(my_score)
    best = winner_array
    result = []
    score = my_score
    for i in range(3):
        if score > winner_array[i]:
            result.append(score)
            score = winner_array[i]
        else:
            result.append(winner_array[i])

    if my_score == result[0]:
        pygame.image.save(my_img,where+'_imgs/output/score1.jpg')
        #cv2.imwrite(where+'_imgs/output/score1.jpg', my_img)

    return result
            

def winnerRewardScreen(screen, my_screen_img, my_person_img, my_qr_img, score1_img, reward_winners, my_score,reward_limit_time, content_num):
    my_person_img = pygame.transform.scale(my_person_img, (int(W/2), int(H/2)))
    my_qr_img = pygame.transform.scale(my_qr_img, (int(H/4), int(H/4)))
    score1_img = pygame.transform.scale(score1_img, (int(H/4)-4, int(H/4-10)))
    reward_bl = pygame.image.load('./ui_imgs/winner_reward.png')
    reward_bl = pygame.transform.scale(reward_bl, (int(W), int(H)))
                  
    text1 = fontObj.render(str(reward_winners[0]),20,YELLOW)
    text2 = fontObj.render(str(reward_winners[1]),20,WHITE)
    text3 = fontObj.render(str(reward_winners[2]),20,WHITE)
    text4 = fontObj.render(str(my_score),20,WHITE)
    

    screen.blit(my_screen_img, (0,0))
    screen.blit(reward_bl, (0,0))
    screen.blit(score1_img, (W/7,H/4-22)) # 1등 사진
    screen.blit(my_qr_img, (W/7, H/2-20))
    screen.blit(my_person_img, (W/3+24, H/4-18))

    #123등 점수
    screen.blit(text1,(150,53))
    screen.blit(text2,(257,53))
    screen.blit(text3,(363,53))
    screen.blit(text4,(505,53))

    #리워드 남은시간
    textSurfaceObj = fontObjBig.render(str(reward_limit_time), True, WHITE)
    screen.blit(textSurfaceObj, (533,403))

    #db
    #dbManager.addInfos(content_num, 20, 1)
    #dbManager.addScore(content_num, my_score)
    return screen

def drawingRewardScreen(screen, my_screen_img, my_person_img, my_qr_img, reward_limit_time):
    
    my_person_img = pygame.transform.scale(my_person_img, (int(W/2), int(H/2)))
    my_qr_img = pygame.transform.scale(my_qr_img, (int(H/4), int(H/4)))
    reward_gr = pygame.image.load('./ui_imgs/drawing_reward_green.png')
    reward_gr = pygame.transform.scale(reward_gr, (int(W), int(H)))
    
    screen.blit(my_screen_img, (0,0))
    screen.blit(reward_gr, (0,0))
    screen.blit(my_qr_img, (W/7-2, H/2-18))
    screen.blit(my_person_img, (W/3+24, H/4-18))
    
    textSurfaceObj = fontObjBig.render(str(reward_limit_time), True, WHITE)
    screen.blit(textSurfaceObj, (530,19))

    #db
    #dbManager.addInfos(0, 20, 1)
    #dbManager.addScore(0, 0)
    return screen

def gameScreen(StoU,recvXY):
    
    screen = pygame.display.set_mode((W,H))
    pygame.init()
    pygame.mixer.init()
    TARGET_FPS = 60
    clock = pygame.time.Clock()
    
    SELECT_TIME = 5
    WARNING_TIME = 2
    PLAY_TIME = 20
    REWARD_TIME = 5
    global fontObj
    fontObj = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 32)
    global fontObjBig
    fontObjBig = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 56)  

    arrow = pygame.image.load('./ui_imgs/arrow.png')
    arrow = pygame.transform.scale(arrow, (int(100), int(100)))
    select_bg = pygame.image.load('./ui_imgs/select_background.png')
    select_bg = pygame.transform.scale(select_bg, (int(W), int(H)))

    runned = False
    thresh_done=False
    center = (0,0)
    mode = "SLEEP_MODE"
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
    
    while True:
        ret, frame = frontcam.read()
        cv2.imshow("now", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.destroyWindow("now")
            break

    frame = np.flip(frame, axis =1)
    
    background_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    background_img = cv2.GaussianBlur(background_img, (5,5),255)
    sleep_start_time = time.time()
    cam_on = True
    
    while True:
        global playMusic, playReward, music, rewardMusic


        #center = pygame.mouse.get_pos()

                    
        screen.fill(BLACK)
        
        if recvXY.poll():
            center = recvXY.recv()
                

        if mode == "SLEEP_MODE":
            
            screen.blit(sleep_img,(0,0))
            
        elif mode == "SELECT_MODE":
            
            if playMusic == False:
                music.play()
                playMusic = True
            #선택 배경
            screen.blit(select_bg, (0,0))
            
            select_limit_time = SELECT_TIME -int(time.time()-select_start_time)
            if select_limit_time < 0:
                music.stop()
                playMusic = False
                if center[0] <int((W-innerW)/2)+innerW/3:

                    firework = funcFirework.FireFunc(screen)
                    mode = "FIREWORK" # [ FIREWORK ]
                    winner_mode = "FIREWORK"
                    
                elif center[0] <int((W-innerW)/2)+innerW/3*2:

                    drawing = funcDrawing.Drawing(screen)
                    mode = "DRAWING" # [ DRAWING ]
                    winner_mode = "DRAWING"
                    
                else: 

                    virus = funcVirus.VirusFunc(screen)
                    mode = "VIRUS" # [ VIRUS ]
                    winner_mode = "VIRUS"
                
                
                #pygame.display.flip()  # 화면 전체를 업데이트
                clock.tick(TARGET_FPS)
                cv2.waitKey(1000)
                screen.fill(BLACK)
                play_start_time = time.time()
                play_start = True

            else:
                #선택시간 출력 
                   
                if center[0] <int((W-innerW)/2)+innerW/3:
                    pygame.draw.rect(screen, RED, [int((W-innerW)/2), H-innerH,innerW/3, H],5) #x,y,w,h [FIREWORK]
                    
                elif int((W-innerW)/2)+innerW/3 <= center[0] <int((W-innerW)/2)+innerW/3*2:
                    pygame.draw.rect(screen, RED, [int((W-innerW)/2)+innerW/3, H-innerH, innerW/3, H],5) # [DRAWING]
                    
                elif int((W-innerW)/2)+innerW/3*2 <= center[0] < int((W-innerW)/2)+innerW:
                    pygame.draw.rect(screen, RED, [int((W-innerW)/2)+innerW/3*2, H-innerH, innerW/3, H],5) # [VIRUS]

                screen.blit(blank, (0,0))
                textSurfaceObj = fontObj.render(str(select_limit_time), True, BLACK)
                screen.blit(textSurfaceObj, (191,35))
                screen.blit(arrow, (center[0]-50, center[1]-50))
                
            if cam_on :
                ret, frame = frontcam.read() #배경캡쳐 됨
                #cv2.imshow("screen",frame)
                
        elif mode == "REWARD_MODE":
            reward_limit_time = REWARD_TIME -int(time.time()-reward_start_time)
            if reward_limit_time < 0:
                reward_start = False
                select_start = False
                mode = "SLEEP_MODE"#playReward = False

            else:
                if playReward == False:
                    rewardMusic.play()
                    playReward = True
                    
                if winner_mode == "FIREWORK" :
                    winnerRewardScreen(screen, my_screen_img, my_person_img, my_qr_img, score1_img, reward_winners, my_score,reward_limit_time,1)
                    
                    
                elif winner_mode == "VIRUS":
                    winnerRewardScreen(screen, my_screen_img, my_person_img, my_qr_img, score1_img, reward_winners, my_score,reward_limit_time,2)


                elif winner_mode == "DRAWING":                    
                    screen = drawingRewardScreen(screen, my_screen_img, my_person_img, my_qr_img, reward_limit_time)
                    
                                        
                
                
        else:   #[컨텐츠 실행 처리]
            play_limit_time = PLAY_TIME -int(time.time()-play_start_time)
            ret, frame = frontcam.read()
            playReward = False
            if play_limit_time < 0: #리워드로 넘어가야됨 -----> 수정) Play_start == False

                if winner_mode == "FIREWORK" : #------------------DB upload 섹션
                    # 서버에 사진 넣기 (사용자 다운로드 용도)
                    img_upload.upload_img('Firework','./firework_imgs/output/screenshot.jpg','./firework_imgs/output/popimage.jpg','./firework_imgs/output/qr_popimage.jpg')
                    
                    my_score = firework.points.p_fw

                    my_person_img = pygame.image.load('./firework_imgs/output/popimage.jpg')
                    
                    firework_winners = comparingScore(firework_winners, my_score, my_person_img, 'firework')
                    reward_winners = firework_winners
                    
                    my_screen_img = pygame.image.load('./firework_imgs/output/screenshot.jpg')
                    my_qr_img = pygame.image.load('./firework_imgs/output/qr_popimage.jpg')
                    score1_img = pygame.image.load('./firework_imgs/output/score1.jpg')
                    
                elif winner_mode == "VIRUS":
                    cv2.imwrite('./virus_imgs/output/popimage.jpg',frame)
                    # 서버에 사진 넣기 (사용자 다운로드 용도)
                    img_upload.upload_img('Virus','./virus_imgs/output/screenshot.jpg','./virus_imgs/output/popimage.jpg','./virus_imgs/output/qr_popimage.jpg')
                    
                    my_score = virus.d_virus
                    
                    my_person_img = pygame.image.load('./virus_imgs/output/popimage.jpg')
                    
                    virus_winners = comparingScore(virus_winners, my_score, my_person_img, 'virus')
                    reward_winners = virus_winners

                    my_screen_img = pygame.image.load('./virus_imgs/output/screenshot.jpg')
                    my_qr_img = pygame.image.load('./virus_imgs/output/qr_popimage.jpg')
                    score1_img = pygame.image.load('./virus_imgs/output/score1.jpg')

                elif winner_mode == "DRAWING":
                    # 서버에 사진 넣기 (사용자 다운로드 용도)
                    img_upload.upload_img('Drawing','./drawing_imgs/output/screenshot.jpg','./drawing_imgs/output/popimage.jpg','./drawing_imgs/output/qr_popimage.jpg')
                    
                    my_person_img = pygame.image.load('./drawing_imgs/output/popimage.jpg')
                    my_screen_img = pygame.image.load('./drawing_imgs/output/screenshot.jpg')
                    my_qr_img = pygame.image.load('./drawing_imgs/output/qr_popimage.jpg')
                    



                play_start = False
                mode = "REWARD_MODE"
                reward_start_time = time.time()
                    
                
                
            else:                
                if mode == "FIREWORK":
                    if ret:
                        frame = np.flip(frame, axis = 1)
                        firework.fireMain(background_img, frame)
                        textSurfaceObj = fontObj.render(str(play_limit_time), True, WHITE)
                        screen.blit(textSurfaceObj, (470,408))
                        screen.blit(pygame.image.load("./ui_imgs/time_limit.png"),(500,402))

                elif mode == "VIRUS":
                    if ret:
                        frame = np.flip(frame, axis = 1)
                        virus.virusMain(background_img, frame)
                        textSurfaceObj = fontObj.render(str(play_limit_time), True, BLACK)
                        screen.blit(textSurfaceObj, (470,408))
                        screen.blit(pygame.image.load("./ui_imgs/time_limit.png"),(500,402))
                        
                elif mode == "DRAWING": #발자국 찍기
                    if ret:
                        frame = np.flip(frame, axis = 1)
                        drawing.drawingMain(center,frame, play_limit_time)
                        textSurfaceObj = fontObj.render(str(play_limit_time), True, BLACK)
                        screen.blit(textSurfaceObj, (470,408))
                        screen.blit(pygame.image.load("./ui_imgs/time_limit.png"),(500,402))
                
                
                
                        
                        
       
        if StoU.poll():
            RECV_MODE = StoU.recv()
            
            if RECV_MODE == "SLEEP_MODE":
                mode = "SLEEP_MODE"
                select_start = False
                if cam_on == True:
                    sleep_start_time = time.time()
                    
                
            elif RECV_MODE == "SELECT_MODE":
                if select_start == False : #셀렉트 타임아웃때문에 필요한 select_time
                    select_start = True
                    select_start_time = time.time()
                    
                    if cam_on ==False:
                        screen.fill(BLACK)
                        textSurfaceObj = fontObj.render("LOADING", True, WHITE)
                        screen.blit(textSurfaceObj, (210,H/2))
                        pygame.display.flip()  # 화면 전체를 업데이트
                                
                        frontcam = cv2.VideoCapture('6.mp4')
                        frontcam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
                        frontcam.set(cv2.CAP_PROP_FRAME_WIDTH,W)
                        frontcam.set(cv2.CAP_PROP_FRAME_HEIGHT,H)
                        
                        cam_on = True
                        mode = "SLEEP_MODE"

                    elif cam_on ==True:
                        mode = "SELECT_MODE"
                        
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
##sendXY.send((3"DRAWING",240))
##gameScreen(StoU,recvXY)
