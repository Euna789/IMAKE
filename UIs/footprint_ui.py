import cv2

import pygame
from pygame.locals import *
from pygame.display import *

global W
W= 640
global H
H= 480

bg_img = pygame.image.load('background.jpg')

# video capture image  
user_img = pygame.image.load('popimage.jpg')
user_img = pygame.transform.scale(user_img, (int(W/3), int(H/3)))

# content screenshot image               
content_img = pygame.image.load('screenshot.jpg')
content_img = pygame.transform.scale(content_img, (int(W/3), int(H/3)))

# qr code image
qr_img = pygame.image.load('qr_popimage.png')
qr_img = pygame.transform.scale(qr_img, (int(W/9),int(W/9)))

# instructions
fun_ = pygame.image.load('havingFun.png')
fun_ = pygame.transform.scale(fun_, (int(W/3), 40))
read_ = pygame.image.load('readQR.png')
read_ = pygame.transform.scale(read_, (int(2.5*(W/3)),40))

s = pygame.Surface((W,H))
s.set_alpha(128)
s.fill((0,0,0))

display = (W, H)
screen = pygame.display.set_mode(display, DOUBLEBUF)
pygame.init()

screen.blit(bg_img,(0,0))
screen.blit(s,(0,0))
screen.blit(user_img,(W/9,H/4))
screen.blit(content_img,(5*W/9,H/4))
screen.blit(qr_img, (7*W/9, 370))
##screen.blit(fun_, (W/9, 320))
##screen.blit(read_, (W/9, 370))
screen.blit(read_, (W/9, 320))
screen.blit(fun_, (W/3,60))
pygame.display.flip()
