# img_upload.py, upload image to server

import requests
import qrcode
import cv2
import numpy as np
import time
import qrcode
from bs4 import BeautifulSoup

server_ip = "http://10.200.37.130:8000"

def upload_img(filename):

    my_img = cv2.imread(filename)
    ctime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))

    files = {'img':open(filename,'rb')}
    values = {'name':ctime,'title':'컨텐츠제목'}

    r = requests.post(server_ip+"/upload/", files = files, data = values)
    
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a")
    leng = len(links)
    
    my_img = links[leng-1]['href']        
    view_url = server_ip + my_img
    
    qr = qrcode.make(view_url)
    qr.save('output/qr_popimage.jpg')



    
