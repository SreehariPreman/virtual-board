import cv2
import os
import HandTrackingModule as htm
import numpy as np

brushsize = 15
erasersize=100

drawColor=(0,0,255)

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
imgcanvas=np.zeros((720,1280,3),np.uint8)


detector=htm.handDetector(detectionCon=0.85)

while True:

#1.  import image
    success,img = cap.read()
    img=cv2.flip(img,1)
    cv2.rectangle(img,(20,10),(320,100),(0,0,255),cv2.FILLED)
    cv2.rectangle(img, (340, 10), (650, 100), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (670, 10), (980, 100), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (1000, 10), (1270, 100), (0, 0, 0))
    cv2.putText(img,'ERASER',(1080,85),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)





#2. find hand landmarks
    img=detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)

    if len(lmlist)!=0:
        print(lmlist)

        #tip of 2 fingers
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]

#3. check which finger is up
        fingers=detector.fingersUp()
        #print(fingers)

#4.if selection mode - two finger is up
        if fingers[1] and fingers[2]:
            xp, yp = 0,0
            print('selection Mode')

            #checking for the click
            if y1 < 130:
                if 20 < x1 < 320:

                    drawColor = (0, 0, 255)
                elif 340 < x1 < 650:

                    drawColor = (0, 255, 0)
                elif 670 < x1 < 980:

                    drawColor = (240, 80, 0)
                elif 1000 < x1 < 1270:

                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)

#5. if drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1),20, drawColor, cv2.FILLED)

            print('Drawing Mode')

            if xp==0 and yp==0:
                xp,yp == x1,y1

            xp, yp = x1, y1
            if drawColor==(0,0,0):

                cv2.line(img, (xp, yp), (x1, y1), drawColor, erasersize)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawColor, erasersize)

            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushsize)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawColor, brushsize)

    imgGray=cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgcanvas)




    img=cv2.addWeighted(img,1 ,imgcanvas,0.5,0)
    cv2.imshow('image',img)
    #cv2.imshow('paint',box)
    #cv2.imshow('canvas',imgcanvas)
    cv2.waitKey(1)



