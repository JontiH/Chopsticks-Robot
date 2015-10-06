# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:39:27 2015

@author: Jonti
"""
import sys
import cv2
import numpy as np
import chopsticks as cs
import serial
import time


def main():
    cap = cv2.VideoCapture(0)
    previousState = 0
    counterLimit = 30
    counter = 0
    isSplit = False
    ai =  cs.Solver(1,1,1,1)
    
    while(1):
        madeMove = False
        ret, frame = cap.read()
        
        # Our operations on the frame come here
        height, width = frame.shape[:2] 
        
       
        
        
        frame, leftHandNumber, rightHandNumber, gRight,bLeft,gUp,bUp  = contourGen(frame)
        
        state = determineState(width, height, gRight,bLeft,gUp,bUp)
        
        if isSplit:
            state = 6
            
        
        if state != previousState :
            counter = 0
        elif state!= 0:
            counter += 1
            
        if counter > counterLimit :
            counter = 0            
            
            if ai.isValidMove(state) is False:
                 state = 7
            else:
                print "valid!"
            if state == 1 :
                isSplit = True
            elif state == 6 :
                if ai.split(leftHandNumber, rightHandNumber) is True:
                 #  ret = ai.split(leftHandNumber, rightHandNumber)
                    
                    
                    
                    
                    isSplit = False
                    madeMove = True
                else:
                    counter = counterLimit/2
                    print "lol"
                    
            else :
                ai.normalMove(state)
                madeMove = True
                
            drawSupporting(frame, width, height, state, leftHandNumber, rightHandNumber, (0,255,0))
            
           
            
        else:
            drawSupporting(frame, width, height, state, leftHandNumber, rightHandNumber, (0,0,255))
            
        if madeMove is True:
            AILeft, AIRight, output = ai.makeNextMove()
            print "%i, %i, %i, " %(AILeft, AIRight, output)
            sys.stdout.flush()
            
            ser=serial.Serial(port='\\.\COM3', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
            time.sleep(3)
            serialOut = str(AILeft) + str(AIRight) + str(output)
            print " serial"
            print serialOut
            ser.write(serialOut)
            ser.close()
        previousState = state
        
        
        
        

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def contourGen(frame):
    
        upperS = 255
        upperV = 255

        blueLowerBGR = (0, 0, 0)
        blueUpperBGR = (255, 150, 50)
        
        greenLowerBGR = (0, 0, 0)
        greenUpperBGR = (150, 255, 150)
        
        lowerB = (101,150,50)
        upperB = (145,upperS,upperV)
        
        lowerG = (50,50, 0)
        upperG = (100,upperS,upperV)
        
        blue = cv2.inRange(frame,blueLowerBGR,blueUpperBGR)
        green = cv2.inRange(frame,greenLowerBGR,greenUpperBGR)
        
        
        newBlue = cv2.bitwise_and(frame,frame, mask =blue)
        newGreen = cv2.bitwise_and(frame,frame, mask =green)
        
        hueBlue = cv2.cvtColor(newBlue, cv2.COLOR_BGR2HSV)
        hueGreen = cv2.cvtColor(newGreen, cv2.COLOR_BGR2HSV)

        
        B = cv2.inRange(hueBlue,lowerB,upperB)
        G = cv2.inRange(hueGreen,lowerG,upperG)
        
        kernel = np.ones((3,3),np.uint8)
        
        erosionB = cv2.erode(B,kernel,iterations = 1)
        dilationB = cv2.dilate(erosionB,kernel,iterations =2)
       
        erosionG = cv2.erode(G,kernel,iterations = 1)
        dilationG = cv2.dilate(erosionG,kernel,iterations =2)
       
        #dt = cv2.distanceTransform(dilation,cv2.DIST_L2,3)
        #cv2.normalize(dt, dt, 0,1, cv2.NORM_MINMAX)
        resultB,contoursB,hierarchyB = cv2.findContours(dilationB, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        resultG,contoursG,hierarchyG = cv2.findContours(dilationG, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width = frame.shape[:2]        
        
        contourListB = sorted(contoursB, key = cv2.contourArea, reverse = True)[:10]
        
        circleListB = []
        for c in contourListB:
           # print cv2.contourArea(c)
            if cv2.contourArea(c) > 500:
                circleListB.append(c)
        bLeft = width
        bUp = height
        for c in circleListB:
            
            m = cv2.moments(c)
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            if cx < bLeft:
                bLeft = cx
            if cy < bUp:
                bUp = cy
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)
           
        #print len(circleListB)
        
        contourListG = sorted(contoursG, key = cv2.contourArea, reverse = True)[:10]
        
        circleListG = []
        for c in contourListG:
           # print cv2.contourArea(c)
            if cv2.contourArea(c) > 500:
                circleListG.append(c)
        gRight = 0
        gUp = height
        for c in circleListG:
            
            #calculate xy of coloured spots
            
            m = cv2.moments(c)
        
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            if cx > gRight:
                gRight = cx
            if cy < gUp:
                gUp = cy
            
            cv2.drawContours(frame, [c], -1, (255, 0, 0), 3)
            
        blueNumber = len(circleListB)
        greenNumber = len(circleListG)
        
     
    
        return frame, greenNumber, blueNumber, gRight,bLeft,gUp,bUp;
    
def determineState(width, height, gRight,bLeft,gUp,bUp) :
        
        #none
        state = 0
        
        
        if bLeft > gRight  and bLeft < width and gRight > 0:
                #split
                state = 1
        elif bUp > height/2 and bUp < height:
                # r -> r
            if bLeft > width/2 and bLeft < width :
                state = 3
            else:
                # r -> r
                state = 2
        elif gUp > height/2 and gUp < height:
                
            if gRight < width/2 and gRight > 0:
                #l -> r
                state = 4
            else:
                # l ->l
                state = 5
        
        
        return state
def drawSupporting(frame, width, height, state, greenNumber, blueNumber, colour):
    
        moveDescriptor = "none"
        
        if state == 1:
            moveDescriptor = "split"
        if state == 3:
            moveDescriptor = "right --> right"
        if state == 2:
            moveDescriptor = "right --> left"
        if state == 4:
            moveDescriptor = "left --> left"
        if state == 5:
            moveDescriptor = "left --> right"
        if state == 7:
            moveDescriptor = "invalid move"
     
     
     
        cv2.line(frame,(width/2,0),(width/2,height),(0,0,0),5)
        cv2.line(frame,(0,height/2),(width,height/2),(0,0,0),5)
      
        cv2.putText(frame,moveDescriptor,(width/2 - 200 ,50), cv2.FONT_HERSHEY_PLAIN, 2,colour,2,cv2.LINE_AA)
        cv2.putText(frame,'%i' %blueNumber,(10,50), cv2.FONT_HERSHEY_PLAIN, 4,(255,120,120),2,cv2.LINE_AA)
        cv2.putText(frame,'%i' %greenNumber,(width- 50,50), cv2.FONT_HERSHEY_PLAIN, 4,(120,255,120),2,cv2.LINE_AA)

    
if __name__ == "__main__":main()