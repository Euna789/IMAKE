import cv2
from multiprocessing import Process, Queue, Pipe

global W
W= 640
global H
H= 480

global innerW
innerW= W
global innerH
innerH= H

display = (W, H)
TARGET_FPS = 60

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out_up = cv2.VideoWriter('output_up.avi',fourcc, 25.0, (W,H))

def preprocess(frame):

    frame = cv2.bilateralFilter(frame, 9, 75, 75)

    ret, frame = cv2.threshold(frame, 30, 255, cv2.THRESH_BINARY_INV)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)

    frame[:,:,0] = cv2.equalizeHist(frame[:,:,0])

    aft_hist = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)

    frame = cv2.cvtColor(aft_hist, cv2.COLOR_BGR2GRAY)

    ret, frame = cv2.threshold(frame, 14, 255, cv2.THRESH_BINARY_INV)
    
    return frame

   
def upperCam(UtoS,sendXY):
    none_count = 0 
    NONE_SEC = 20 #사람 없는 거 최대 몇 초까지 보고 절전모드할 지
    latest_location = (0,0)
    valid_circle = 0
    
    Sleep = True
    '''
    frontcam = cv2.VideoCapture(1)
    frontcam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    frontcam.set(cv2.CAP_PROP_FRAME_WIDTH,W)
    frontcam.set(cv2.CAP_PROP_FRAME_HEIGHT,H)
    '''
    
    video = cv2.VideoCapture(1)
    while True:

        ret, orig_frame = video.read()
        if not ret:
            video = cv2.VideoCapture('video2.mp4')
            continue
        '''
        ret, orig_frame = frontcam.read()
        if not ret:
            continue
        '''
        out_up.write(orig_frame)
        
        orig_frame = cv2.resize(orig_frame, display)

        gray = preprocess(orig_frame)
        gray = cv2.Canny(gray, 20, 100)
        circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1.12,minDist=80,\
                               param1=50,param2=30,minRadius=0,maxRadius=70)

        valid_circle = 0
        if circles is not None:
            if (Sleep == False) and (UtoS.poll()==True):
                if UtoS.recv() =="WHICH_CONTENT?":
                    if latest_location[0] <int((W-innerW)/2)+innerW/2:
                        UtoS.send("FIRE_WORK")
                        cv2.putText(orig_frame, "FIRE_WORK", (200,200), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 2)
        
                    else:
                        UtoS.send("VIRUS")
                        cv2.putText(orig_frame, "VIRUS", (200,200), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 2)
                        
                
            for c in circles[0,:]:
                center = (c[0],c[1])
                radius = c[2]
                
                if orig_frame[int(c[1]),int(c[0])][0]<15 and orig_frame[int(c[1]),int(c[0])][1]<15 and orig_frame[int(c[1]),int(c[0])][2]<15:
                #if orig_frame[int(c[1])-10:int(c[1])+10][int(c[0])-10:int(c[0])+10][0]<50 and orig_frame[int(c[1])-10:int(c[1])+10][int(c[0])-10:int(c[0])+10][1]<50 and orig_frame[int(c[1])-10:int(c[1])+10][int(c[0])-10:int(c[0])+10][2]<50:
            
                    if (W-innerW)/2 < c[0] < int((W-innerW)/2)+innerW and H-innerH < c[1] < H: # [ 컨텐츠 선택 창 생성 ] -gamescreen에 선택 창 띄우도록 함#
                        valid_circle += 1
                        UtoS.send("SELECT_MODE") # -어느 구역에 있는지 디텍트해서 알려줘야함. 그림그리기의 경우는 따로 알려줘야 함. 제한시간 내에 선택하도록 함.
                        
                        Sleep = False
                        none_count = 0
                        latest_location=center
                        sendXY.send(latest_location)
                        
                        cv2.circle(orig_frame,center,radius,(0,255,0),2)# 바깥원
                        #cv2.circle(orig_frame,center,2,(0,0,255),3)     # 중심원
                    else:
                        cv2.putText(orig_frame, "Not In The Bound", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0), 2)
                        cv2.circle(orig_frame,center,radius,(0,0,255),2)# 바깥원
                        none_count+=1

                else:
                    #cv2.putText(orig_frame, "Not A Head", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0), 2)
                    none_count+=1
                
        elif circles is None:
            if Sleep == False: #오류로 인해서 머리가 잠시 안 잡힐때 또는 사용자가 나간지 얼마 안될 때
                none_count += 1
                '''cv2.putText(orig_frame, "Not-detected", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0), 2)'''

         
        if Sleep == True: #[ 절전모드 ] - gamescreen에 절전 창 뜨도록 함
            UtoS.send("SLEEP_MODE")
            cv2.putText(orig_frame, "Sleep Mode", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 2)
            
        elif Sleep == False:
            if none_count > TARGET_FPS*NONE_SEC:
                Sleep=True
                valid_circle = 0
                UtoS.send("SLEEP_MODE")
                #none_count = 0 # 0으로 재세팅

            if valid_circle > 1:
                UtoS.send("ONE_PERSON_WARNING")
                       
        
        cv2.rectangle(orig_frame, (int((W-innerW)/2), H-innerH),(int((W-innerW)/2)+innerW, H), (255,0,0),2) #인식 사각형
        txt = str(none_count)+","+str(TARGET_FPS*NONE_SEC)
        #cv2.putText(orig_frame, txt, (100, 200), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 2)
        cv2.imshow("frame", orig_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            video.release()
            out_up.release()
            break

        cv2.waitKey(1)
     
