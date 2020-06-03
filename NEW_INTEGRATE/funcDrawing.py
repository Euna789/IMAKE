import sys
import pygame
import TM as detect
import cv2 as cv
import random
from pygame.locals import *

class Drawing:
##    cap = cv.VideoCapture('6.mp4')
##    cap.set(3,640)
##    cap.set(4,480)

    #initialization
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100,-16,2,512)
    #screen = pygame.display.set_mode((640, 480),FULLSCREEN | HWSURFACE | DOUBLEBUF)
    clock = pygame.time.Clock()
    
    def __init__(self, screen):
        self.screen=screen

        self.animal_flag = 0

        self.mousepos=[]
        self.animals=[]
        self.colors=[]
        self.opacity=[]
        self.done=False #done game

        self.color_now=None
        self.animal_now='cat'
        self.opacity_now=300
        self.highest_len = 0

        #spill time
        self.spill_y=0
        self.spill_g=0
        self.spill_s=0
        self.spill_p=0

        #paint time
        self.time=0

        #guide window
        self.guide_count=0
        self.guide2_count=0

        #camera
        self.pos_prev = (60, 60)
        self.pos_now = (60, 60)

    def blit_alpha(self,target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
        
    def check_collision(self,pos,pos_now,distance):
        if -distance<pos_now[0]-pos[0]<distance and -distance<pos_now[1]-pos[1]<distance:
            return True
        else:
            return False

    def imgLoad(self,name):
        return pygame.image.load('./drawing_imgs/sprites/'+name+'.png')

    def imgLoad1(name):
        return pygame.image.load('./drawing_imgs/sprites/'+name+'.png')

    def drawObject(self,animal, XY, opacity):
        self.blit_alpha(self.screen,animal, XY,opacity)



    broom_flag=0

    # PAINT IMG
    guide1=imgLoad1('guide_1')
    guide2=imgLoad1('guide_2')

    broom_1=imgLoad1('broom1')
    broom_2=imgLoad1('broom2')

    paints_size=60
    
    bucket_y_img=imgLoad1('bucket_y')
    bucket_g_img=imgLoad1('bucket_g')
    bucket_p_img=imgLoad1('bucket_p')
    bucket_s_img=imgLoad1('bucket_s')
    bucket_y_3=imgLoad1('bucket_y_3')
    bucket_g_3=imgLoad1('bucket_g_3')
    bucket_p_3=imgLoad1('bucket_p_3')
    bucket_s_3=imgLoad1('bucket_s_3')

    bucket_y_2=imgLoad1('bucket_y_2')
    bucket_g_2=imgLoad1('bucket_g_2')
    bucket_p_2=imgLoad1('bucket_p_2')
    bucket_s_2=imgLoad1('bucket_s_2')

    horse_face=imgLoad1('horse_face')
    bird_face=imgLoad1('bird_face')
    cat_face=imgLoad1('cat_face')
    
    animal_init = ['cat','horse', 'bird']
    

    #color
    YELLOW=(255,255,0)
    GREEN=(0,255,0)
    SKYBLUE=(23,219,255)
    PINK=(255,0,255)


    #coordinate
    bucket_y=(150,100)
    yellow=(220,100)
    bucket_g=(100,200)
    green=(170,200)
    bucket_s=(380,300)
    skyblue=(450,300)
    pink=(650,300)
    bucket_p=(580,300)
    broom=(580,100)

    distance=40

    X=0
    Y=0

    def drawingMain(self, center, img, time):

        if time == 0:
            cv.imwrite('./drawing_imgs/output/popimage.jpg', img)
            pygame.image.save(self.screen,"./drawing_imgs/output/screenshot.jpg")
            
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                done = True
                

        
        self.screen.fill((0,0,0))
        self.screen.blit(pygame.image.load('./drawing_imgs/sprites/background.png'),(0,0))
        
        self.pos_prev = self.pos_now
        # get hand point from video
##        ret,img = cap.read()
          
##        if ret == False:
##            continue

##        points = (center[0],center[1])
        points=pygame.mouse.get_pos()
        
        #cv.imshow('result', img)
        # if person head is found
        if type(points) is tuple:
            #self.pos_now = (points[0]*1.3-60, points[1]*1.3-60)
            self.pos_now = center

        # if user goes out of the screen, change animal
        if not(40 < self.pos_now[0] < 600 and 40 < self.pos_now[1] < 435) and \
           (40 < self.pos_prev[0]< 600 and 40 < self.pos_prev[1] < 435): 
            self.animal_flag += 1
            self.animal_now = self.animal_init[self.animal_flag%3]
            sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/'+self.animal_now+'.ogg')
            sfx1.play()

        '''
        if (0<self.pos_now[0]<640 and 0 < self.pos_now[1] < 480) and not(0<self.pos_prev[0]<640 and 0<self.pos_prev[1]<480):
            if self.animal_now=='cat':
                sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/cat.ogg')
                #sfx1.set_volume(0.5)
                sfx1.play()
            elif self.animal_now=='horse':
                sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/horse.ogg')
                #sfx1.set_volume(0.5)
                sfx1.play()
            else:
                sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/bird.ogg')
                #sfx1.set_volume(0.5)
                sfx1.play()
        '''


            # check if user collided to buckets
        if self.check_collision(self.bucket_y,self.pos_now,self.distance):
            self.spill_y+=1
            if self.spill_y!=0:
                self.color_now='_y'
                self.time=1
                self.opacity_now=300
                sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/splash.ogg')
                #sfx1.set_volume(0.5)
                sfx1.play()
        elif self.check_collision(self.bucket_g,self.pos_now,self.distance):
            self.spill_g+=1
            if self.spill_g!=0:
                self.color_now='_g'
                self.time=1
                self.opacity_now=300
                sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/splash.ogg')
                #sfx1.set_volume(0.5)
                sfx1.play()
        elif self.check_collision(self.bucket_s,self.pos_now,self.distance):
            self.spill_s+=1
            if self.spill_s!=0:
                self.color_now='_s'
                self.time=1
                self.opacity_now=300
                sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/splash.ogg')
                #sfx1.set_volume(0.5)
                sfx1.play()
        elif self.check_collision(self.bucket_p,self.pos_now,self.distance):
            self.spill_p+=1
            if self.spill_p!=0:
                self.color_now='_p'
                self.time=1
                self.opacity_now=300
                sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/splash.ogg')
                #sfx1.set_volume(0.5)
                sfx1.play()
        
        if self.time>0:
            self.time+=1
            self.opacity_now-=10
            if self.time==30:
                self.color_now='time_over'
                self.time=0
                
        # broom img
        if self.broom_flag==0:
            self.screen.blit(self.broom_1,(self.broom[0]-int(67/2),self.broom[1]-int(116/2)))

        # draw stand up/spilled paint bucket depending on 'spill_' bool
        if self.spill_y==0:#YELLO
            self.screen.blit(self.bucket_y_img,(self.bucket_y[0]-int(self.paints_size/2),self.bucket_y[1]-int(self.paints_size/2)))
        elif self.spill_y>0 and self.spill_y<3:
            self.screen.blit(self.bucket_y_2,(self.bucket_y[0]-int(self.paints_size/2),self.bucket_y[1]-int(self.paints_size/2)))
            self.spill_y+=1
        else :
            self.screen.blit(self.bucket_y_3,(self.bucket_y[0]-int(self.paints_size/2),self.bucket_y[1]-int(self.paints_size/2)))
            self.spill_y+=1
            if self.spill_y>20:
                self.spill_y=0
                self.X=random.randint(50,600)
                self.Y=random.randint(50,430)
                self.yellow=(self.X,self.Y)
                self.bucket_y=(self.yellow[0]-70,self.yellow[1])
        
        if self.spill_g==0:#GREEN
            self.screen.blit(self.bucket_g_img,(self.bucket_g[0]-int(self.paints_size/2),self.bucket_g[1]-int(self.paints_size/2)))
        elif self.spill_g>0 and self.spill_g<3:
            self.screen.blit(self.bucket_g_2,(self.bucket_g[0]-int(self.paints_size/2),self.bucket_g[1]-int(self.paints_size/2)))  
            self.spill_g+=1
        else :
            self.screen.blit(self.bucket_g_3,(self.bucket_g[0]-int(self.paints_size/2),self.bucket_g[1]-int(self.paints_size/2)))
            self.spill_g+=1
            if self.spill_g>20:
                self.spill_g=0
                self.X=random.randint(50,600)
                self.Y=random.randint(50,430)
                self.green=(self.X,self.Y)
                self.bucket_g=(self.green[0]-70,self.green[1])
        
        if self.spill_s==0:#SKYBLUE
            self.screen.blit(self.bucket_s_img,(self.bucket_s[0]-int(self.paints_size/2),self.bucket_s[1]-int(self.paints_size/2)))
        elif self.spill_s>0 and self.spill_s<3:
            self.screen.blit(self.bucket_s_2,(self.bucket_s[0]-int(self.paints_size/2),self.bucket_s[1]-int(self.paints_size/2)))
            self.spill_s+=1
        else :
            self.screen.blit(self.bucket_s_3,(self.bucket_s[0]-int(self.paints_size/2),self.bucket_s[1]-int(self.paints_size/2)))
            self.spill_s+=1
            if self.spill_s>20:
                self.spill_s=0
                self.X=random.randint(50,600)
                self.Y=random.randint(50,430)
                self.skyblue=(self.X,self.Y)
                self.bucket_s=(self.skyblue[0]-70,self.skyblue[1])
        
        if self.spill_p==0:#PINK
            self.screen.blit(self.bucket_p_img,(self.bucket_p[0]-int(self.paints_size/2),self.bucket_p[1]-int(self.paints_size/2)))
        elif self.spill_p>0 and self.spill_p<3:
            self.screen.blit(self.bucket_p_2,(self.bucket_p[0]-int(self.paints_size/2),self.bucket_p[1]-int(self.paints_size/2)))
            self.spill_p+=1
        else :
            self.screen.blit(self.bucket_p_3,(self.bucket_p[0]-int(self.paints_size/2),self.bucket_p[1]-int(self.paints_size/2)))
            self.spill_p+=1
            if self.spill_p>20:
                self.spill_p=0
                self.X=random.randint(50,600)
                self.Y=random.randint(50,430)
                self.pink=(self.X,self.Y)
                self.bucket_p=(self.pink[0]-70,self.pink[1])

        # ERASE
        if self.check_collision(self.broom,self.pos_now,self.distance):
            self.mousepos.clear()
            self.animals.clear()
            self.opacity.clear()
            self.screen.blit(self.broom_2,(self.broom[0]-int(89/2),self.broom[1]-int(143/2)))
            sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/erase.ogg')
            sfx1.set_volume(0.5)
            sfx1.play()
            self.broom_flag=1
        else:
            self.broom_flag=0
            

        # user img
        
        #screen.blit(flower,(pos_now[0]-int(flower_size/2),pos_now[1]-int(flower_size/2)))


        
            
        # if user did not touch any bucket yet, no footstep printing
        if self.color_now is None:
            #guide window blit
            if self.guide_count>=20:
                self.screen.blit(self.guide1,(150,100))
                if self.spill_y != 0 and self.spill_s != 0 and self.spill_g != 0 and self.spill_p != 0:
                    self.screen.blit(self.guide2,(150,100))
                    self.guide2_count += 1
            if self.guide2_count > 0:
                self.screen.blit(self.guide2,(150,100))
                self.guide2_count += 1
                if self.guide2_count >= 15:
                    self.guide2_count = 0
                    self.guide_count = 0
            pygame.display.update()
            
            #continue
            #return ####################

        elif self.color_now is not 'time_over':
            self.mousepos.append(self.pos_now)
            mousepos_count = len(self.mousepos)
            self.animals.append((detect.rotate_img(self.animal_now+self.color_now,self.mousepos[mousepos_count-2],self.mousepos[mousepos_count-1])))
            self.opacity.append(self.opacity_now)
            '''
            sfx1 = pygame.mixer.Sound('./drawing_imgs/sound/step.ogg')
            sfx1.set_volume(0.5)
            sfx1.play()
            '''
            
        # draw footsteps on screen
        for i in range(len(self.mousepos)):
            self.drawObject(self.animals[i],self.mousepos[i],self.opacity[i])

        if len(self.mousepos) > self.highest_len:
            self.highest_len = len(self.mousepos)
            cv.imwrite('./drawing_imgs/output/popimage.jpg', img)
            pygame.image.save(self.screen,"./drawing_imgs/output/screenshot.jpg")


        #player image (face)
        if self.animal_now=='cat':
            self.screen.blit(self.cat_face,(self.pos_now[0]-20,self.pos_now[1]-20))
        elif self.animal_now=='horse':
            self.screen.blit(self.horse_face,(self.pos_now[0]-20,self.pos_now[1]-20))
        else:
            self.screen.blit(self.bird_face,(self.pos_now[0]-10,self.pos_now[1]-10))           
    
        #guide window blit
        if self.guide_count>=20:
            self.screen.blit(self.guide1,(150,100))
            if self.spill_y != 0 and self.spill_s != 0 and self.spill_g != 0 and self.spill_p != 0:
                self.screen.blit(self.guide2,(150,100))
                self.guide2_count += 1 
        if self.guide2_count > 0:
            self.screen.blit(self.guide2,(150,100))
            self.guide2_count += 1
            if self.guide2_count >= 15:
                self.guide2_count = 0
                self.guide_count = 0

        if self.opacity_now <= 10:
            self.guide_count += 1
        else:
            self.guide_count = 0


        if time == 0:
            cv.imwrite('./drawing_imgs/output/popimage.jpg', img)
            pygame.image.save(self.screen,"./drawing_imgs/output/screenshot.jpg")
        
        #pygame.display.flip()
            
