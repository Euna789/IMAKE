# -*- coding: utf-8 -*-
import sys
import pygame
import time
from pygame.locals import *
from pygame.display import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import *
import math
import cv2
import numpy as np
from collections import Counter
import threading
from img_upload import *


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
W= 640
global H
H= 480
display = (W, H)

loop = True

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
#------------------------------------------------------------------------


virus = pygame.image.load('virus.png')
virus_L = pygame.image.load('virus_L.png')
virus_M = pygame.image.load('virus_M.png')
virus_S = pygame.image.load('virus_S.png')

hand_img1 = pygame.image.load('bg.png')
hand_img1 = pygame.transform.scale(hand_img1, (W,H))

back_png = pygame.image.load('back.png')
back_png = pygame.transform.scale(back_png, (W,H))

end_png = pygame.image.load('end.png')

TARGET_FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode(display, pygame.FULLSCREEN )

pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound("Rain.wav")
chan1 = pygame.mixer.Channel(0)

# set sound to initial value
sound.set_volume(1)

chan1.play(sound,-1)
chan1.set_volume(1.0, 1.0)    

num = 0
d_virus = 0
colored = np.zeros((W,H,3))
viruses = []

LRsize = int(W/2)*int(H/2)
fullSize = W*int(H/2)
##instruction
def setVolume(person):
    exists = np.where(person == 255)  #255 means an existence of person
    cnt = Counter(exists[1])
    cnt = cnt.most_common()
    cnt_len = len(cnt)
    if cnt_len > 1:
        mid_cnt = int(cnt_len / 2)
        cnt_half = cnt[:mid_cnt]
        min_cnt = min(cnt_half)
        max_cnt = max(cnt_half)
        man_size = max_cnt[0] - min_cnt[0]
        exists_rat = man_size / W
    else:
        exists_rat= 0
    
    exists_len = len(exists[0])
    exist_l = np.where(person[:,:int(W/2)]==255)
    exist_l_len = len(exist_l[0])
    exist_r = np.where(person[:,int(W/2):]==255)
    exist_r_len = len(exist_r[0])

    l_rat = exist_l_len / LRsize
    r_rat = exist_r_len / LRsize

    return (min(1,exists_rat * l_rat), min(1, exists_rat * r_rat))



#--------------------virus 클래스 정의 ----------------------------
class Virus:
    x, y = 0, 0
    touched_B = False
    touched_N =0
    radius = 40
    color = (255,0,0)
    my_virus = virus_L
    tick = 0
    change = randint(1,7)

    def __init__ (self):
        self.x = randint(50,W-50)
        self.y = randint(50,H-50)
        self.effect = pygame.mixer.Sound("gig.wav")
        self.effect.set_volume(1)   #set volume(value) or set_volume(left, right)
        self.effect.play(1)
        
    def draw(self):
        screen.blit(self.my_virus, (self.x-self.radius, self.y-self.radius))
        #pygame.draw.circle(screen, self.color, (self.x, self.y) , self.radius)
        
    def update(self, mask):
        if self.tick%self.change==0:
            self.tick = 0
            if(self.x > 50 and self.x<W-50 and self.y>50 and self.y<H-50):
                self.x += randint(-10,10)
                self.y += randint(-10,10)
            else:
                self.x = randint(50,W-50)
                self.y = randint(50,H-50)
        self.tick += 1
    
        if (mask[v.x][v.y] == 0) and (self.touched_B==False):
        ##사람 없고 && 터치된 기록 x
            self.touched_B = False
            
        elif (mask[v.x][v.y] == 0) and (self.touched_B== True):
        ##사람 없고 && 터치된 기록 o
            self.touched_B = False
            
        elif (mask[v.x][v.y] == 255) and (self.touched_B==False):
        ##사람 있고 && 터치된 기록 x
            self.touched_B = True
            self.touched_N += 1
            self.radius-=10
            if (self.radius == 20):
                self.my_virus = virus_M
                self.effect.set_volume(0.5)
            if (self.radius == 10):
                self.my_virus = virus_S
                self.effect.set_volume(0.3)
            self.effect.play(1)
                
        elif (mask[v.x][v.y] == 255) and (self.touched_B==True):
        ##사람 있고 && 터치된 기록 o
            self.touched=True
            
        if self.touched_N > 3:
            self.effect.set_volume(0.2)
            self.effect.play(1)
            return True

        return False
        
#--------------------main-----------------------------------------
    
##instruction
ins = pygame.image.load('instruction.png').convert_alpha()
#font
myfont = pygame.font.SysFont("comicsansms",20, bold = True)

##-----------카메라 셋업 ~~ --------------------------

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,H)
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=200, detectShadows=False)

runned = False

def nothing(x):
    pass

##---------- ~~ 카메라 셋업 ------------------------
while True:            
    ##---------- 백그라운드 대비 사람 이미지 처리 ~~ ---------
    while runned == False:
        ret, frame = cap.read()
        cv2.imshow("original", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'): # s버튼 누르고
            break
        
    ret, frame = cap.read() #배경캡쳐 됨

    if runned == False: #백그라운드 이미지 처리
        background_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        background_img = cv2.GaussianBlur(background_img, (5,5),255)
        runned = True

    ##---------- ~~ 백그라운드 대비 사람 이미지 처리  ---------
    elif runned == True:
        timer(0)
        break

 ##--------------------게임의 상태를 업데이트하는 부분--------------------------
while loop == True:
    screen.fill(BLACK)  # 화면을 검은색으로 지운다
    screen.blit(back_png,(0,0))
    screen.blit(hand_img1,(0,0))
    #font size was 10
    text1 = myfont.render("Dead viruses: " + str(d_virus),20,(0,128,0))
    screen.blit(text1,(10,10))
    
    for event in pygame.event.get(): #종료버튼
        if event.type == QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
            
    ret, frame = cap.read() #배경캡쳐 됨
    
    if (len(viruses) < 8) :
        temp = Virus() #init <-- x,y,qty
        viruses.append(temp)
        
        #print(temp.x,",",temp.y)

    this_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    this_img = cv2.GaussianBlur(this_img, (5,5),0)      
    abdiff = cv2.absdiff(this_img, background_img)

    _, thresh_img = cv2.threshold(abdiff, 35, 255, cv2.THRESH_BINARY)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel2, 3)
    border = cv2.dilate(opening, kernel2, iterations=3)
    border = border - cv2.erode(border, None)

    temp = np.rot90(border)
    m_temp = np.flipud(temp)
    exists = np.where(thresh_img == 255)  #255 means an existence of person

    temp = np.rot90(thresh_img)
    masking = temp     
    mask = np.flipud(masking)
    cv2.imshow("ya",thresh_img)
    
    me = pygame.surfarray.make_surface(mask).convert()
    view = 255-mask        
    view = pygame.surfarray.make_surface(view).convert()        
    view.set_alpha(80)
    screen.blit(view,(0,0))
    
    for i in range(len(viruses)-1, -1, -1):
        v = viruses[i]
        v.draw()
        if v.update(mask):
            d_virus += 1
            del(viruses[i])
            
    if(len(exists[0])==0):
        #안내창 보여주기
        screen.blit(ins,(108,176))
        d_virus = 0
        chan1.set_volume(1.0, 1.0)
    else:
        a = thresh_img.copy()
        l_sound, r_sound = setVolume(a)
        chan1.set_volume(l_sound, r_sound)
    
##------------------------화면 업데이트 ------------------------------

    pygame.display.flip()  # 화면 전체를 업데이트
    clock.tick(TARGET_FPS)  # 프레임 수 맞추기

#------------------------------- time out----------------------------

pygame.image.save(screen,"output/screenshot.jpg")
cv2.imwrite('output/popimage.jpg', frame)

##upload_img('output/popimage.jpg')

font = pygame.font.SysFont('Consolas', 20)

qr_img = pygame.image.load('output/qr_popimage.jpg')
qr_img = pygame.transform.scale(qr_img, (int(W/4), int(H/4)))

time_left = 5

while True:
    time_left -= 1
    if time_left > -1:
        screen.blit(end_png, (0,0))   # 불투명 검정 화면

        out_screen = pygame.image.load('output/screenshot.jpg')
        out_person = pygame.image.load('output/popimage.jpg')
        score1 = pygame.image.load('output/score1.jpg')
        score1 = pygame.transform.scale(score1, (int(W/4), int(H/4)))
        out_screen = pygame.transform.scale(out_screen, (int(W/4), int(H/4)))
        out_person = pygame.transform.scale(out_person, (int(W/4), int(H/4)))
        text1 = myfont.render("1 st: " + str(d_virus),20,(0,128,0))
        screen.blit(text1,(10,120))
        text2 = myfont.render("2 nd: " + str(d_virus),20,(0,128,0))
        screen.blit(text2,(10,140))
        text3 = myfont.render("3 rd: " + str(d_virus),20,(0,128,0))
        screen.blit(text3,(10,160))

        screen.blit(score1, (0,0)) # 1등 사진
        screen.blit(out_screen, (5,H/2))
        screen.blit(qr_img, (W/2-W/8, H/2))
        screen.blit(out_person, (W-W/4-5, H/2))

        text = font.render("Time left: "+str(time_left), True, (255,255,255))
        screen.blit(text, (200, 400))
        pygame.display.flip()
        time.sleep(1)#making the time interval of the loop 1sec
    else:
        text = font.render("Time Over!!", True, (0,0,0))
        screen.blit(text, (200, 200))
        pygame.display.flip()
        screen.fill((20,20,20))
        break


'''
screen.blit(end_png, (0,0))   # 불투명 검정 화면

out_screen = pygame.image.load('output/screenshot.jpg')
out_person = pygame.image.load('output/popimage.jpg')
score1 = pygame.image.load('output/score1.jpg')
score1 = pygame.transform.scale(score1, (int(W/4), int(H/4)))
out_screen = pygame.transform.scale(out_screen, (int(W/4), int(H/4)))
out_person = pygame.transform.scale(out_person, (int(W/4), int(H/4)))
text1 = myfont.render("1 st: " + str(d_virus),20,(0,128,0))
screen.blit(text1,(10,120))
text2 = myfont.render("2 nd: " + str(d_virus),20,(0,128,0))
screen.blit(text2,(10,140))
text3 = myfont.render("3 rd: " + str(d_virus),20,(0,128,0))
screen.blit(text3,(10,160))




#------------------------ 최종 화면 업데이트 -------------------------

screen.blit(score1, (0,0)) # 1등 사진
screen.blit(out_screen, (5,H/2))
screen.blit(qr_img, (W/2, H/2))
screen.blit(out_person, (W-W/4-5, H/2))
pygame.display.flip()
'''


cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
        
