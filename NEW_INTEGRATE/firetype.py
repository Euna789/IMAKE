import pygame
from pygame.locals import *
from random import *
import math
import numpy as np

W = 640
H = 480

global p_fw
p_fw = 0
global highest_y
highest_y = 480

#-----------------------Ray
class Ray:
    dest_x, dest_y = 0,  0
    x,y = W,H
    color = (0,0,0)
    
    def __init__(self, x,y, color, screen):
        self.dest_x = x
        self.dest_y = y
        self.x = x
        self.y = H
        self.color = color
        self.speed = randint(5,8)
        self.screen = screen

    def check_me(self, mouse):
        return (self.x-10 < mouse[0] <self.x+10) and (self.y - 10 < mouse[1] < self.y+10)  

    def update(self, mask):
        pygame.draw.line(self.screen, self.color, (self.x,self.y), (self.x,self.y+40),1)     
        self.y -= self.speed

        self.dest_x = self.x
        self.dext_y = self.y
        
        if self.y < 0 or self.x < 0 or self.x >= 640 or self.y >= 480 :
            return False
        else:
            
            return mask[math.floor(self.y)][math.floor(self.x)] == 255  

#-------------------------Particle
class Particle:
    def __init__ (self, x, y, vx, vy, color,G, screen):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.G = G
        self.screen = screen
       
    def draw(self):
        pygame.draw.ellipse(self.screen, self.color, [int(self.x),int(self.y),2,2], 1)
            
    def update(self):
        self.vy += self.G
        self.x += self.vx
        self.y += self.vy

        return self.y > H or self.x < 0 or self.x > W  #|| 연산자
    
#-------------------------Fire making function
def Draw(fire_arr):
    for i in range(len(fire_arr)-1, -1, -1):
        fire_arr[i].update()
        fire_arr[i].draw()
    
#-------------------------Fires    
class Fire_type1:
    ######################
    # bursts_in_a_circle #
    ######################
    def __init__ (self, x, y, screen):
        self.x = x
        self.y = y
        self.vy = 0.16
        self.color = (randint(100,255),randint(100,255),randint(100,255))
        self.thickness = randint(1,3)
        
        self.ray = Ray(x,y,self.color, screen)
        self.ray_bool = False

        self.outter = []
        self.inner = []
        self.count = 0

        self.screen = screen
        self.photo = False

        self.effect = pygame.mixer.Sound("./firework_imgs/going_up.wav")
        self.effect.set_volume(1)
        self.effect.play(1)
       
    def makeoutter(self):
        for i in range (randint(50,200)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.outter.append(Particle(self.ray.x, self.ray.y, 3*math.sin(r), 3*math.cos(r) ,self.color, 0.08, self.screen))

    def makeinner(self):
        color = (randint(50,255),randint(50,255), randint(50,255))
        for i in range (randint(300,500)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.inner.append(Particle(self.ray.x, self.ray.y+20, R*math.sin(r), R*math.cos(r), color, 0.17, self.screen))
            
    def draw(self):
        if (self.count < 50):
            Draw(self.outter)
        
        if ( 50 > self.count > 20):
            Draw(self.inner)

    def update(self, mask):
        
        if self.ray_bool: #마우스에 닿았을 때
            if self.count==0: #바깥쪽 폭죽 생성 전
                global p_fw
                p_fw += 1
                global highest_y
                if self.y < highest_y:
                    highest_y = self.y
                    self.photo = True
                    
                self.x = self.ray.dest_x
                self.y = self.ray.dest_y
                self.makeoutter()
                self.effect = pygame.mixer.Sound("./firework_imgs/splash.wav")
                self.effect.set_volume(0.7)
                self.effect.play(1)

            else: #바깥쪽 폭죽 생성 후
                self.draw()
            self.count += 1
                
        elif ( self.ray.y < 0 ): # 터치하지 못하고 지나가 없어졌을 경우
            return True #boolean
            
        else: #마우스에 아직 안 닿았을 때
            self.ray_bool = self.ray.update(mask)
        
        self.y += self.vy

        if self.count == 19: #안쪽 폭죽
            self.makeinner()

        return (self.count==51) #boolean ; 카운트 51되면 true

class Fire_type2:
    ###########################
    # circle and circle burst #
    ###########################
    def __init__ (self, x, y, screen):
        self.x = x
        self.y = y
        self.vy = 0.16
        self.color = (randint(100,255),randint(100,255),randint(100,255))
        self.thickness = randint(1,3)
        
        self.ray = Ray(x,y,self.color, screen)
        self.ray_bool = False

        self.outter = []
        self.inner = []
        self.count = 0

        self.screen = screen
        self.photo = False
       
        self.effect = pygame.mixer.Sound("./firework_imgs/going_up.wav")
        self.effect.set_volume(1)
        self.effect.play(1)
        
    def makeoutter(self):
        for i in range (randint(50,200)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.outter.append(Particle(self.ray.x, self.ray.y, R*math.sin(r), R*math.cos(r) ,self.color, 0.08, self.screen))

    def makeinner(self):
        color = (randint(50,255),randint(50,255), randint(50,255))
        for i in range (randint(300,500)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.inner.append(Particle(self.ray.x, self.ray.y+20, R*math.sin(r), R*math.cos(r), color, 0.17, self.screen))
            
    def draw(self):
        if (self.count < 50):
            Draw(self.outter)
        
        if ( 50 > self.count > 20):
            Draw(self.inner)

    def update(self, mouse):
        
        if self.ray_bool: #마우스에 닿았을 때
            if self.count==0: #바깥쪽 폭죽 생성 전
                global p_fw
                p_fw += 1
                global highest_y
                if self.y < highest_y:
                    highest_y = self.y
                    self.photo = True
                self.x = self.ray.dest_x
                self.y = self.ray.dest_y
                self.makeoutter()
                self.effect = pygame.mixer.Sound("./firework_imgs/splash.wav")
                self.effect.set_volume(0.7)
                self.effect.play(1)

            else: #바깥쪽 폭죽 생성 후
                self.draw()
            self.count += 1
                
        elif ( self.ray.y < 0 ): # 터치하지 못하고 지나가 없어졌을 경우
##                print("miss")
                return True #boolean
            
        else: #마우스에 아직 안 닿았을 때
            self.ray_bool = self.ray.update(mouse)
        
        self.y += self.vy

        if self.count == 19: #안쪽 폭죽
            self.makeinner()

        return (self.count==51) #boolean ; 카운트 51되면 true
            
class Fire_type3:
    #####################
    # 요가파이어 스타일 # ## 레어
    #####################
    def __init__ (self, x, y, screen):
        self.x = x
        self.y = y
        self.vy = 0.16
        self.color = (randint(100,255),randint(100,255),randint(100,255))
        self.thickness = randint(1,3)
        
        self.ray = Ray(x,y,self.color, screen)
        self.ray_bool = False

        self.outter = []
        self.inner = []
        self.count = 0

        self.screen = screen
        self.photo = False
       
        self.effect = pygame.mixer.Sound("./firework_imgs/going_up.wav")
        self.effect.set_volume(1)
        self.effect.play(1)
        
    def makeoutter(self):
        for i in range (randint(50,200)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.outter.append(Particle(self.ray.x, self.ray.y, randint(2,4)*math.sin(r), randint(2,4)**math.cos(r) ,self.color, 0.08, self.screen))

    def makeinner(self):
        #self.color = (randint(50,255),randint(50,255), randint(50,255))
        for i in range (randint(300,500)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.inner.append(Particle(self.ray.x, self.ray.y, R*math.sin(r), R*math.cos(r), self.color, 0.17, self.screen))
            
    def draw(self, mouse):
        if self.count<15:
            self.ray.color = self.color
            self.ray.update(mouse)
        if (self.count < 50):
            Draw(self.outter)
        if (15<self.count<65):
            Draw(self.inner)
        

    def update(self, mouse):
        
        if self.ray_bool: #마우스에 닿았을 때
            if self.count==0: #바깥쪽 폭죽 생성 전
                global p_fw
                p_fw += 1
                global highest_y
                if self.y < highest_y:
                    highest_y = self.y
                    self.photo = True
                self.makeoutter()
                self.color = (randint(50,255),randint(50,255), randint(50,255))
                
                self.effect = pygame.mixer.Sound("./firework_imgs/splash.wav")
                self.effect.set_volume(0.7)
                self.effect.play(1)

            else: #바깥쪽 폭죽 생성 후
                self.draw(mouse)
            self.count += 1
                
        elif ( self.ray.y < 0 ): # 터치하지 못하고 지나가 없어졌을 경우
##                print("miss")
                return True #boolean
            
        else: #마우스에 아직 안 닿았을 때
            self.ray_bool = self.ray.update(mouse)

        if self.count == 15:
            self.makeinner()
            
        self.y += self.vy
        return (self.count==51) #boolean ; 카운트 51되면 true

class Fire_type4:
    ###############################
    # 외국 장미 아이스크림 스타일 #
    ###############################
    def __init__ (self, x, y, screen):
        self.x = x
        self.y = y
        self.vy = 0.16
        self.color = (randint(100,255),randint(100,255),randint(100,255))
        self.thickness = randint(1,3)
        
        self.ray = Ray(x,y,self.color, screen)
        self.ray_bool = False

        self.outter = []
        self.inner = []
        self.count = 0

        self.screen = screen
        self.photo = False
       
        self.effect = pygame.mixer.Sound("./firework_imgs/going_up.wav")
        self.effect.set_volume(1)
        self.effect.play(1)
        
    def makeoutter(self):
        for i in range (randint(50,200)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.outter.append(Particle(self.ray.x, self.ray.y, randint(2,4)*math.sin(r), randint(2,4)*math.cos(r) ,self.color, 0.08, self.screen))

    def makeinner(self):
        #self.color = (randint(50,255),randint(50,255), randint(50,255))
        for i in range (randint(150,300)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.inner.append(Particle(self.ray.x, self.ray.y, R*math.sin(r)/2, R*math.cos(r)/2, self.color, 0.08, self.screen))
            
    def draw(self):
        if self.count<15:
            self.ray.color = self.color
        if (self.count < 50):
            Draw(self.outter)
            Draw(self.inner)

    def update(self, mouse):
        
        if self.ray_bool: #마우스에 닿았을 때
            if self.count==0: #바깥쪽 폭죽 생성 전
                global p_fw
                p_fw += 1
                global highest_y
                if self.y < highest_y:
                    highest_y = self.y
                    self.photo = True
                self.makeoutter()
                self.color = (randint(100,255),randint(100,255),randint(100,255))
                self.makeinner()
                self.effect = pygame.mixer.Sound("./firework_imgs/splash.wav")
                self.effect.set_volume(0.7)
                self.effect.play(1)
            else: #바깥쪽 폭죽 생성 후
                self.draw()
            self.count += 1
                
        elif ( self.ray.y < 0 ): # 터치하지 못하고 지나가 없어졌을 경우
##                print("miss")
                return True #boolean
            
        else: #마우스에 아직 안 닿았을 때
            self.ray_bool = self.ray.update(mouse)
            
        return (self.count==51) #boolean ; 카운트 51되면 true

class Fire_type5:
    #########################
    # a circle and a circle #
    #########################
    def __init__ (self, x, y, screen):
        self.x = x
        self.y = y
        self.vy = 0.16
        self.color = (randint(100,255),randint(100,255),randint(100,255))
        self.thickness = randint(1,3)
        
        self.ray = Ray(x,y,self.color, screen)
        self.ray_bool = False

        self.outter = []
        self.inner = []
        self.count = 0

        self.screen = screen
        self.photo = False
       
        self.effect = pygame.mixer.Sound("./firework_imgs/going_up.wav")
        self.effect.set_volume(1)
        self.effect.play(1)
        
    def makeoutter(self):
        for i in range (randint(50,200)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.outter.append(Particle(self.ray.x, self.ray.y, 3*math.sin(r), 3*math.cos(r) ,self.color, 0.08, self.screen))

    def makeinner(self):
        color = (randint(50,255),randint(50,255), randint(50,255))
        for i in range (randint(300,600)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.inner.append(Particle(self.ray.x, self.ray.y+20, 3*math.sin(r), 3*math.cos(r), color, 0.17, self.screen))
            
    def draw(self):
        if (self.count < 50):
            Draw(self.outter)
        
        if ( 50 > self.count > 20):
            Draw(self.inner)

    def update(self, mouse):
        
        if self.ray_bool: #마우스에 닿았을 때
            if self.count==0: #바깥쪽 폭죽 생성 전
                global p_fw
                p_fw += 1
                global highest_y
                if self.y < highest_y:
                    highest_y = self.y
                    self.photo = True
                self.x = self.ray.dest_x
                self.y = self.ray.dest_y
                self.makeoutter()
                self.effect = pygame.mixer.Sound("./firework_imgs/splash.wav")
                self.effect.set_volume(0.7)
                self.effect.play(1)

            else: #바깥쪽 폭죽 생성 후
                self.draw()
            self.count += 1
                
        elif ( self.ray.y < 0 ): # 터치하지 못하고 지나가 없어졌을 경우
##                print("miss")
                return True #boolean
            
        else: #마우스에 아직 안 닿았을 때
            self.ray_bool = self.ray.update(mouse)
        
        self.y += self.vy

        if self.count == 19: #안쪽 폭죽
            self.makeinner()

        return (self.count==51) #boolean ; 카운트 51되면 true

class Fire_type6:
    ################
    # basic circle #
    ################
    def __init__ (self, x, y, screen):
        self.x = x
        self.y = y
        self.vy = 0.16
        self.color = (randint(100,255),randint(100,255),randint(100,255))
        self.thickness = randint(1,3)
        
        self.ray = Ray(x,y,self.color, screen)
        self.ray_bool = False

        self.outter = []
        self.inner = []
        self.count = 0

        self.screen = screen
        self.photo = False

        self.effect = pygame.mixer.Sound("./firework_imgs/going_up.wav")
        self.effect.set_volume(1)
        self.effect.play(1)
        
    def makeoutter(self):
        for i in range (randint(200,500)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.outter.append(Particle(self.ray.x, self.ray.y, R*math.sin(r), R*math.cos(r) ,self.color, 0.08, self.screen))

    def draw(self):
        if (self.count < 30):
            Draw(self.outter)          

    def update(self, mouse):
        
        if self.ray_bool: #마우스에 닿았을 때
            if self.count==0: #바깥쪽 폭죽 생성 전
                global p_fw
                p_fw += 1
                global highest_y
                if self.y < highest_y:
                    highest_y = self.y
                    self.photo = True
                self.makeoutter()
                self.effect = pygame.mixer.Sound("./firework_imgs/splash.wav")
                self.effect.set_volume(0.7)
                self.effect.play(1)

            else: #바깥쪽 폭죽 생성 후
                self.draw()
            self.count += 1
                
        elif ( self.ray.y < 0 ): # 터치하지 못하고 지나가 없어졌을 경우
##                print("miss")
                return True #boolean
            
        else: #마우스에 아직 안 닿았을 때
            self.ray_bool = self.ray.update(mouse)
        
        self.y += self.vy

        return (self.count==51) #boolean ; 카운트 51되면 true

class Fire_type7:
    ##########
    # planet #
    ##########
    def __init__ (self, x, y, screen):
        self.x = x
        self.y = y
        self.vy = 0.16
        self.color = (randint(100,255),randint(100,255),randint(100,255))
        self.thickness = randint(1,3)
        
        self.ray = Ray(x,y,self.color, screen)
        self.ray_bool = False

        self.outter = []
        self.inner = []
        self.sparkle = []
        self.back = []
        self.count = 0

        self.screen = screen
        self.photo = False

        self.mask = np.zeros(shape = (H,W))
        self.mask[80][int(W/2)] = 255
       
        self.effect = pygame.mixer.Sound("./firework_imgs/going_up.wav")
        self.effect.set_volume(1)
        self.effect.play(1)
        
    def makeoutter(self):
        for i in range (randint(100,250)):
            r = uniform(0, 2*math.pi) #float
            self.outter.append(Particle(self.ray.x+randint(1,5), self.ray.y+randint(1,2), 8*math.sin(r), 2*math.cos(r) ,self.color, 0.08, self.screen))
            self.outter.append(Particle(self.ray.x-randint(1,5), self.ray.y+randint(1,2), 8*math.sin(r), 2*math.cos(r) ,self.color, 0.08, self.screen))
            self.outter.append(Particle(self.ray.x+randint(1,5), self.ray.y-randint(1,2), 8*math.sin(r), 2*math.cos(r) ,self.color, 0.08, self.screen))
            self.outter.append(Particle(self.ray.x-randint(1,5), self.ray.y-randint(1,2), 8*math.sin(r), 2*math.cos(r) ,self.color, 0.08, self.screen))

    def makeinner(self):
        color = (randint(50,255),randint(50,255), randint(50,255))
        for i in range (randint(500,650)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, math.pi) #float
            self.inner.append(Particle(self.ray.x, self.ray.y-5, R*math.sin(r), R*math.cos(r), color, 0.10, self.screen))

    def makeSparkle(self):
        color = (randint(50,255),randint(50,255), randint(50,255))
        xx = randint(50, 580)
        yy = randint(50, 350)
        for i in range (randint(50,150)):
            r = uniform(0, 2*math.pi) #float
            R = uniform(0, 0.1*math.pi) #float
            self.sparkle.append(Particle(xx, yy, R*math.sin(r), R*math.cos(r), color, 0.17, self.screen))

    def backSparkle(self):
        color = (randint(50,255),randint(50,255), randint(50,255))
        xx = randint(50, 580)
        yy = randint(50, 350)
        for i in range (randint(50,150)):
            r = uniform(0, 2*math.pi) #float
            xx = randint(50, 580)
            yy = randint(50, 350)
            self.back.append(Particle(xx, yy, math.sin(r), math.cos(r), color, 0.07, self.screen))

    def draw(self):
        if (self.count < 30):
            Draw(self.outter)
            Draw(self.inner)
            Draw(self.sparkle)
            Draw(self.back)

    def update(self, mouse):
        if self.ray_bool: #마우스에 닿았을 때
            if self.count==0: #바깥쪽 폭죽 생성 전
                global highest_y
                if self.y < highest_y:
                    highest_y = self.y
                    self.photo = True
                self.makeoutter()
                self.makeinner()
                self.backSparkle()
                self.effect = pygame.mixer.Sound("./firework_imgs/splash.wav")
                self.effect.set_volume(0.7)
                self.effect.play(1)

            else: #바깥쪽 폭죽 생성 후
                self.draw()
                
            self.count += 1
                
        elif ( self.ray.y < 0 ): # 터치하지 못하고 지나가 없어졌을 경우
                return True #boolean
            
        else: #마우스에 아직 안 닿았을 때
            self.ray_bool = self.ray.update(self.mask)

        
        self.y += self.vy
        
        if self.count > 0 and self.count % 4 == 0:
            #print("make",self.count)
            self.makeSparkle()
        
        return (self.count==51) #boolean ; 카운트 51되면 true
