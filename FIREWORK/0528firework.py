# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import *
import cv2
import numpy as np
import threading

import firetype
#from firetypeSP import Particle, Sparker

#색 정의
BLACK= (0,0,0) #R G B
RED = (255, 0, 0)
GREEN = (255,0, 255)
BLUE = (0, 0, 255)
ORANGE = (255,180,0)
YELLOW = (255,255,0)
YELLOW_A = (255,255,0, 80)
BLUE_A = (0, 0, 255, 127)  # R, G, B, Alpha(투명도, 255 : 완전 불투명)

global W
global H

W = 640
H = 480

loop = True

def random_Fire():
    random = randint(1,6)
    if random == 1:
        temp = firetype.Fire_type1(randint(50,W-50), randint(50,H), screen) #init <-- x,y,qty
        
    elif random == 2:
        temp = firetype.Fire_type2(randint(50,W-50), randint(50,H), screen) #init <-- x,y,qty
        
    elif random == 3:
        temp = firetype.Fire_type3(randint(50,W-50), randint(50,H), screen) #init <-- x,y,qty
        
    elif random == 4:
        temp = firetype.Fire_type4(randint(50,W-50), randint(50,H), screen) #init <-- x,y,qty
        
    elif random == 5:
        temp = firetype.Fire_type5(randint(50,W-50), randint(50,H), screen) #init <-- x,y,qty
        
    elif random == 6:
        temp = firetype.Fire_type6(randint(50,W-50), randint(50,H), screen) #init <-- x,y,qty
        
    fires.append(temp)
    
#--------------------------------TIMER---------------------------------------------
def timer(count):
    count += 1
    tic = threading.Timer(1,timer,args=[count])
    tic.start()

    if count == 50:
        print("timer end")
        global loop
        loop = False
        tic.cancel()

#------------------------------- MAIN ----------------------------
TARGET_FPS = 20
clock = pygame.time.Clock()

display = (W, H)
screen = pygame.display.set_mode(display, DOUBLEBUF)

fires = []
reward = False
pygame.init()
pygame.mixer.init()
num = 0
myfont = pygame.font.SysFont("comicsansms",20, bold = True)
##Background image for showing
bgimage = pygame.image.load('background.png').convert_alpha()
bgimage = pygame.transform.scale(bgimage, (W,H))

##instruction
ins = pygame.image.load('instruction.png').convert_alpha()

##Background image array for checking firework
bg = cv2.imread('background.png')
src = cv2.resize(bg, dsize=(W,H), interpolation = cv2.INTER_AREA)
temp = np.rot90(src)
src=np.flipud(temp)

# 건물의 x, y 경계
arc = cv2.Canny(src, 40, 45)
arc_x = np.where(arc==255)[0]
arc_y = np.where(arc==255)[1]

################################CAMERA########################
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,H)
#fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=200, detectShadows=False)

runned = False

def nothing(x):
    pass

'''
cv2.namedWindow("panel", cv2.WINDOW_NORMAL)
cv2.createTrackbar("Threshold","panel", 0, 255, nothing)
cv2.resizeWindow("panel", 7, 100)

thresh_done=False
'''
################################################################

while True:  # setting background img
    while runned == False:
        ret, frame = cap.read()
        cv2.imshow("original", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
        
    ret, frame = cap.read()
    '''
    if thresh_done==False and runned == True:
        this_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        this_img = cv2.GaussianBlur(this_img, (5,5),0)      
        abdiff = cv2.absdiff(this_img, background_img)
        thresh = cv2.getTrackbarPos("Threshold","panel")
        _, thresh_img = cv2.threshold(abdiff, thresh, 255, cv2.THRESH_BINARY)
        cv2.imshow("threshimg",thresh_img)        
        if cv2.waitKey(1) & 0xFF == ord('d'):
            pygame.mixer.music.load('bgm.mp3')
            pygame.mixer.music.play(-1)
##            screen = pygame.display.set_mode(display, FULLSCREEN|DOUBLEBUF)
            thresh_done=True
    '''    
            
    if runned == False:
        background_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        background_img = cv2.GaussianBlur(background_img, (5,5),0)
        runned = True
        
    elif runned == True:
        timer(0) #start timing
        break

#----------------------------- MAIN GAME --------------------------------------
while loop == True:
    ret, frame = cap.read()

    this_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    this_img = cv2.GaussianBlur(this_img, (5,5),0)      
    abdiff = cv2.absdiff(this_img, background_img)

    _, thresh_img = cv2.threshold(abdiff, 35, 255, cv2.THRESH_BINARY)
    
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel2, 3)
    border = cv2.dilate(opening, kernel2, iterations=3)
    border = border - cv2.erode(border, None)

    temp = np.rot90(border)
    temp = np.flipud(temp)
    exists = np.where(temp == 255)

    screen.fill(BLACK)  # 화면을 검은색으로 지운다
    
    temp = np.rot90(thresh_img)        
    mask = np.flipud(temp)
    me = pygame.surfarray.make_surface(mask).convert()
    me.set_alpha(100)

    if firetype.p_fw % 10 == 0 and not reward:
        print(firetype.p_fw)
        fires.append(firetype.Fire_type7(W/2, H/2, screen)) #init <-- x,y,qty
        reward = True
    
    if (len(fires) < 6) :
        random_Fire()
        
    screen.blit(me,(0,0))   # show player
    
    if(len(exists[0])==0):
        #안내창 보여주기
        screen.blit(ins,(87,40))
    
    for i in range(len(fires)-1, -1, -1):
        f = fires[i]
        me_done=False
        m_x = f.ray.x
        m_y =  f.ray.y
        #건물
        inside = np.where(arc_x == m_x)[0]  #여기수정필요...
        if len(inside) > 0:
            out = min(inside)
            if m_y > arc_y[out]:
                if f.update([0,0]):
                    del(fires[i])
                    me_done=True
                continue
            else:
                if len(exists[0]) > 0:  # 사람이 인식되면
                    for k in range(len(exists[0])):
                        mouse=[exists[0][k],exists[1][k]]
                        if f.ray.check_me(mouse) and not me_done:
                            me_done = True
                            break
                    #폭죽이 마지막까지 출력되었으면 fires에서 삭제
                    if f.update(mouse):
                        reward = False
                        del(fires[i])
                        
                else:
                    #폭죽이 마지막까지 출력되었으면 fires에서 삭제
                    if f.update([0,0]):
                        del(fires[i])
                        me_done=True
                        
        else:
            if len(exists[0]) > 0:
                for k in range(len(exists[0])):
                    mouse=[exists[0][k],exists[1][k]]
                    if f.ray.check_me(mouse) and not me_done:
                        me_done = True
                        break
                if f.update(mouse):
                    del(fires[i])
                        
            else:
                if f.update([0,0]):
                    del(fires[i])
                    me_done=True

        

    text1 = myfont.render("Popped Fireworks: " + str(firetype.p_fw),20,(0,128,0)) # 터뜨린 개수 출력
    screen.blit(text1,(10,10))
                                
    screen.blit(bgimage,(0,0))
    
    pygame.display.flip()  # 화면 전체를 업데이트

    if f.photo:
            cv2.imwrite('output/popimage.jpg', frame)
            pygame.image.save(screen,"output/screenshot.jpg")
            f.photo = False
            
    clock.tick(TARGET_FPS)  # 프레임 수 맞추기

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("out")

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
