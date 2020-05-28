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

#--------------------virus 클래스 정의 ----------------------------
class Virus:
    virus = pygame.image.load('virus.png')
    virus_L = pygame.image.load('virus_L.png')
    virus_M = pygame.image.load('virus_M.png')
    virus_S = pygame.image.load('virus_S.png')
    
    x, y = 0, 0
    touched_B = False
    touched_N =0
    radius = 40
    color = (255,0,0)
    my_virus = virus_L
    tick = 0
    change = randint(1,7)

    def __init__ (self, screen):
        self.x = randint(50,W-50)
        self.y = randint(50,H-50)
        self.effect = pygame.mixer.Sound("gig.wav")
        self.effect.set_volume(1)   #set volume(value) or set_volume(left, right)
        self.effect.play(1)

        self.screen = screen
        
    def draw(self):
        self.screen.blit(self.my_virus, (self.x-self.radius, self.y-self.radius))
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
    
        if (mask[self.x][self.y] == 0) and (self.touched_B==False):
        ##사람 없고 && 터치된 기록 x
            self.touched_B = False
            
        elif (mask[self.x][self.y] == 0) and (self.touched_B== True):
        ##사람 없고 && 터치된 기록 o
            self.touched_B = False
            
        elif (mask[self.x][self.y] == 255) and (self.touched_B==False):
        ##사람 있고 && 터치된 기록 x
            self.touched_B = True
            self.touched_N += 1
            self.radius-=10
            if (self.radius == 20):
                self.my_virus = self.virus_M
                self.effect.set_volume(0.5)
            if (self.radius == 10):
                self.my_virus = self.virus_S
                self.effect.set_volume(0.3)
            self.effect.play(1)
                
        elif (mask[self.x][self.y] == 255) and (self.touched_B==True):
        ##사람 있고 && 터치된 기록 o
            self.touched=True
            
        if self.touched_N > 3:
            self.effect.set_volume(0.2)
            self.effect.play(1)
            return True

        return False

class VirusFunc:
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

    pygame.init()
    pygame.mixer.init()

    hand_img1 = pygame.image.load('bg.png')
    hand_img1 = pygame.transform.scale(hand_img1, (W,H))

    back_png = pygame.image.load('back.png')
    back_png = pygame.transform.scale(back_png, (W,H))

    end_png = pygame.image.load('end.png')

    TARGET_FPS = 60
    clock = pygame.time.Clock()

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

    def __init__(self, screen):
        self.screen = screen
        ##instruction
        self.ins = pygame.image.load('instruction.png').convert_alpha()
        #font
        self.myfont = pygame.font.SysFont("comicsansms",20, bold = True)
    
    ##instruction
    def setVolume(self, person):
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

        l_rat = exist_l_len / self.LRsize
        r_rat = exist_r_len / self.LRsize

        return (min(1,exists_rat * l_rat), min(1, exists_rat * r_rat))
        
    #--------------------main-----------------------------------------
     ##--------------------게임의 상태를 업데이트하는 부분--------------------------
    def virusMain(self, background_img, frame):
        self.screen.fill(self.BLACK)  # 화면을 검은색으로 지운다
        self.screen.blit(self.back_png,(0,0))
        self.screen.blit(self.hand_img1,(0,0))
        #font size was 10
        text1 = self.myfont.render("Dead viruses: " + str(self.d_virus),20,(0,128,0))
        self.screen.blit(text1,(10,10))
        
        for event in pygame.event.get(): #종료버튼
            if event.type == QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
        
        if (len(self.viruses) < 8) :
            temp = Virus(self.screen) #init <-- x,y,qty
            self.viruses.append(temp)
            
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
        self.screen.blit(view,(0,0))
        
        for i in range(len(self.viruses)-1, -1, -1):
            v = self.viruses[i]
            v.draw()
            if v.update(mask):
                self.d_virus += 1
                del(self.viruses[i])
                
        if(len(exists[0])==0):
            #안내창 보여주기
            self.screen.blit(self.ins,(108,176))
            self.d_virus = 0
            self.chan1.set_volume(1.0, 1.0)
        else:
            a = thresh_img.copy()
            l_sound, r_sound = VirusMain.setVolume(self, a)
            self.chan1.set_volume(l_sound, r_sound)
        
    ##------------------------화면 업데이트 ------------------------------

        pygame.display.flip()  # 화면 전체를 업데이트
        self.clock.tick(self.TARGET_FPS)  # 프레임 수 맞추기

    #------------------------------- time out----------------------------
        
        pygame.image.save(self.screen,"output/screenshot.jpg")
        cv2.imwrite('output/popimage.jpg', frame)
