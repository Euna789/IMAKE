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

class FireFunc:
    #색 정의
    BLACK= (0,0,0) #R G B
    '''
    RED = (255, 0, 0)
    GREEN = (255,0, 255)
    BLUE = (0, 0, 255)
    ORANGE = (255,180,0)
    YELLOW = (255,255,0)
    YELLOW_A = (255,255,0, 80)
    BLUE_A = (0, 0, 255, 127)  # R, G, B, Alpha(투명도, 255 : 완전 불투명)
    '''

    global W
    global H

    W = 640
    H = 480

    display = (W, H)

    TARGET_FPS = 60
    clock = pygame.time.Clock()

    fires = []
    reward = False
    pygame.init()
    pygame.mixer.init()
    
    num = 0
    myfont = pygame.font.SysFont("comicsansms",20, bold = True)

    ##Background image array for checking firework
    bg = cv2.imread('firework_imgs/background.png')
    src = cv2.resize(bg, dsize=(W,H), interpolation = cv2.INTER_AREA)
    temp = np.rot90(src)
    src=np.flipud(temp)

    # 건물의 x, y 경계
    arc = cv2.Canny(src, 40, 45)
    arc_x = np.where(arc==255)[0]
    arc_y = np.where(arc==255)[1]

    def __init__(self, screen):
        self.screen = screen

        ##Background image for showing
        self.bgimage = pygame.image.load('firework_imgs/background.png').convert_alpha()
        self.bgimage = pygame.transform.scale(self.bgimage, (W,H))

        ##instruction
        self.ins = pygame.image.load('firework_imgs/instruction.png').convert_alpha()

    def random_Fire(self):
        random = randint(1,6)
        if random == 1:
            temp = firetype.Fire_type1(randint(50,W-50), randint(50,H), self.screen) #init <-- x,y,qty
            
        elif random == 2:
            temp = firetype.Fire_type2(randint(50,W-50), randint(50,H), self.screen) #init <-- x,y,qty
            
        elif random == 3:
            temp = firetype.Fire_type3(randint(50,W-50), randint(50,H), self.screen) #init <-- x,y,qty
            
        elif random == 4:
            temp = firetype.Fire_type4(randint(50,W-50), randint(50,H), self.screen) #init <-- x,y,qty
            
        elif random == 5:
            temp = firetype.Fire_type5(randint(50,W-50), randint(50,H), self.screen) #init <-- x,y,qty
            
        elif random == 6:
            temp = firetype.Fire_type6(randint(50,W-50), randint(50,H), self.screen) #init <-- x,y,qty
            
        self.fires.append(temp)

    def fireMain(self, background_img, frame):
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

        self.screen.fill(self.BLACK)  # 화면을 검은색으로 지운다
        
        temp = np.rot90(thresh_img)        
        mask = np.flipud(temp)
        #print(mask)
        me = pygame.surfarray.make_surface(mask).convert()
        me.set_alpha(100)

        if firetype.p_fw % 10 == 0 and not self.reward and firetype.p_fw>0 :
            print(firetype.p_fw)
            self.fires.append(firetype.Fire_type7(W/2, H/2, self.screen)) #init <-- x,y,qty
            self.reward = True
        
        if (len(self.fires) < 6) :
            self.random_Fire()
            
        self.screen.blit(me,(0,0))   # show player
        
        if(len(exists[0])==0):
            #안내창 보여주기
            self.screen.blit(self.ins,(87,40))
        
        for i in range(len(self.fires)-1, -1, -1):
            f = self.fires[i]
            me_done=False
            m_x = f.ray.x
            m_y =  f.ray.y
            #건물
            inside = np.where(self.arc_x == m_x)[0]  #여기수정필요...
            if len(inside) > 0:
                out = min(inside)
                if m_y > self.arc_y[out]:
                    if f.update([0,0]):
                        del(self.fires[i])
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
                            self.reward = False
                            del(self.fires[i])
                            
                    else:
                        #폭죽이 마지막까지 출력되었으면 fires에서 삭제
                        if f.update([0,0]):
                            del(self.fires[i])
                            me_done=True
                            
            else:
                if len(exists[0]) > 0:
                    for k in range(len(exists[0])):
                        mouse=[exists[0][k],exists[1][k]]
                        if f.ray.check_me(mouse) and not me_done:
                            me_done = True
                            break
                    if f.update(mouse):
                        del(self.fires[i])
                            
                else:
                    if f.update([0,0]):
                        del(self.fires[i])
                        me_done=True

            if f.photo:
                self.screen.blit(self.bgimage,(0,0))
                cv2.imwrite('firework_imgs/output/popimage.jpg', frame)
                pygame.image.save(self.screen,"firework_imgs/output/screenshot.jpg")
                f.photo = False

        text1 = self.myfont.render("Popped Fireworks: " + str(firetype.p_fw),20,(0,128,0)) # 터뜨린 개수 출력
        self.screen.blit(text1,(10,10))
                                    
        self.screen.blit(self.bgimage,(0,0))
        
        pygame.display.flip()  # 화면 전체를 업데이트

        self.clock.tick(self.TARGET_FPS)  # 프레임 수 맞추기
