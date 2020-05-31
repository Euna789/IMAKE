# img_upload.py, upload image to server

import requests
import qrcode
import cv2
import numpy as np
import time
import qrcode
from bs4 import BeautifulSoup

server_ip = "http://10.200.37.130:8000"

def upload_img(program_info, content_img, user_img):
    ctime = time.strftime("%Y, %m, %d, %H, %M", time.localtime(time.time()))
        
    files = {'user_img':open(user_img,'rb'),'content_img':open(content_img,'rb')}
    values = {'user_info':ctime,'program_info':program_info}

    r = requests.post(server_ip+"/upload/", files = files, data = values)
    
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")
    leng = len(links)
    
    my_img = links[leng-1]['href']        
    view_url = server_ip + my_img
    
    qr = qrcode.make(view_url)
    qr.save('output/qr_popimage.jpg')



    
