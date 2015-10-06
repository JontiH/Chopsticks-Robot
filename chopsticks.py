# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:28:56 2015

@author: Jonti
"""
import sys
import time
import serial

class Solver:
    
    myLeftHand = 0
    myRightHand = 0
    theirLeftHand = 0
    theirRightHand = 0
    
    def __init__(self, myLeft, myRight, theirLeft, theirRight):
        
        global myLeftHand
        global myRightHand
        global theirLeftHand
        global theirRightHand
        
        myLeftHand = myLeft
        myRightHand = myRight
        theirLeftHand = theirLeft
        theirRightHand = theirRight
        
        ser=serial.Serial(port='\\.\COM3', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        time.sleep(3)
        serialOut = str(myLeft) + str(myRight) + str(6)
        ser.write(serialOut)
        ser.close()
        time.sleep(2)

        
    def normalMove(self, state):
        global myLeftHand
        global myRightHand
        global theirLeftHand
        global theirRightHand
        
        print "pre start"
        sys.stdout.flush()
        print myLeftHand
        sys.stdout.flush()
        print "middle"
        sys.stdout.flush()
        print myRightHand
        sys.stdout.flush()
        print "state"
        sys.stdout.flush()
        print state
        sys.stdout.flush()
        print "end"
        sys.stdout.flush()
        
        if state == 7:
            return
        
        elif state == 2:
            if myLeftHand > 0:   
               myLeftHand += theirRightHand
            if myLeftHand > 4:
                myLeftHand = 0
        elif state == 3:
            if myRightHand > 0:    
                myRightHand += theirRightHand
            if myRightHand > 4:
                myRightHand = 0
        elif state == 4:
            if myLeftHand > 0:
                myLeftHand += theirLeftHand
            if myLeftHand > 4:
                myLeftHand = 0
        elif state == 5:
            if myRightHand > 0:
                myRightHand += theirLeftHand
            if myRightHand > 4:
                myRightHand = 0
        
        print "post start"
        sys.stdout.flush()
        print myLeftHand
        sys.stdout.flush()
        print "middle"
        sys.stdout.flush()
        print myRightHand
        sys.stdout.flush()
        print "end"
        sys.stdout.flush()  
        
        ser=serial.Serial(port='\\.\COM3', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        time.sleep(2)
        serialOut = str(myLeftHand) + str(myRightHand) + str(6)
        ser.write(serialOut)
        ser.close()
        time.sleep(5)
        
        
         
    
    def split(self, theirLeft,theirRight):
        global theirLeftHand
        global theirRightHand
        print" split!!"
        sys.stdout.flush()
        
        if (theirLeft + theirRight) == (theirLeftHand + theirRightHand) :
            theirLeftHand = theirLeft
            theirRightHand = theirRight 
            ser=serial.Serial(port='\\.\COM3', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
            time.sleep(2)
            serialOut = str(myLeftHand) + str(myRightHand) + str(6)
            ser.write(serialOut)
            ser.close()
            return True
        else :
            return False
              
        
    def isValidMove(self, state):
        global myLeftHand
        global myRightHand
        global theirLeftHand
        global theirRightHand
        
        #todo : check for valid splits
        print "validity statecheck"
        print state
        if state == 3 and (myRightHand == 0 or theirRightHand == 0):
            print "not allowed!!"
            return False
          
        elif state == 2 and (myLeftHand == 0 or theirRightHand == 0):
            print "not allowed!!"
            return False
        elif state == 4 and (myLeftHand == 0 or  theirLeftHand == 0):
            print "not lol!!"
            return False
        elif state == 5 and (myRightHand == 0 or theirLeftHand == 0):
            print "not allowed!!"
            return False
        else :
            return True                    
            
    def makeNextMove(self):
       
        global myLeftHand
        global myRightHand
        global theirLeftHand
        global theirRightHand
        
        print "their left"
        print theirLeftHand
        print "their right"
        print theirRightHand
        
        outputState = 6
        
        if myRightHand == 0 and myLeftHand == 0:
            outputState = 8
        elif theirRightHand == 0 and theirLeftHand == 0:
            outputState = 7
        
        elif theirLeftHand == 1 and theirRightHand ==1:
            if (myLeftHand == 2 and myRightHand ==1 )or (myLeftHand == 1 and myRightHand ==2 ):
                myLeftHand = 3   
                myRightHand = 0
                outputState = 5
            elif myLeftHand ==4 and myRightHand == 0:
                myLeftHand = 3   
                myRightHand = 1
                outputState = 5  
            elif myLeftHand == 4 and myRightHand == 1:
                myLeftHand = 3   
                myRightHand = 2
                outputState = 5  
            elif myLeftHand == 4 and myRightHand == 2 : 
                theirRightHand = 0
                outputState = 2
            elif myLeftHand == 3 and myRightHand == 3:
                theirRightHand = 4
                outputState = 3
            elif (myLeftHand == 3 and myRightHand ==2 )or (myLeftHand == 2 and myRightHand ==3 ):
                theirLeftHand = 4
                if myLeftHand == 3:
                    outputState = 1
                else: 
                    outputState = 4
            
                
            
                
                
            else:
                print "error A "
                
                
        elif (theirLeftHand ==2 and theirRightHand == 0) or (theirLeftHand ==0 and theirRightHand == 2) :
            if myLeftHand == 1 and myRightHand == 1:
                if theirLeftHand == 2:
                    theirLeftHand += myRightHand
                    outputState = 4
                elif theirRightHand == 2:
                    theirRightHand += myLeftHand
                    outputState = 2
                    
            elif (myLeftHand == 3 and myRightHand == 0) or (myLeftHand == 0 and myRightHand == 3):
                if myLeftHand == 3:
                    if theirLeftHand == 2:
                        theirLeftHand = 0
                        outputState = 1
                    else:
                        theirRightHand = 0
                        outputState = 2
                else:
                   if theirLeftHand == 2:
                      theirLeftHand = 0
                      outputState = 4
                   else:
                      theirRightHand = 0
                      outputState = 3 
                
                
            else :
                print "error Z"
        elif (theirLeftHand == 3 and theirRightHand == 0) or (theirLeftHand ==0 and theirRightHand == 3):
            if myLeftHand == 4:
                if theirLeftHand == 3:
                    outputState == 1
                else:
                    outputState == 2
            elif myRightHand == 4:
                if theirLeftHand == 3:
                    outputState == 4
                    theirLeftHand = 0
                else:
                    outputState == 3
                    theirRightHand = 0
            elif (myRightHand == 3 and myLeftHand == 0) or (myRightHand == 0 and myLeftHand == 3):
                if theirLeftHand == 0:
                    theirRightHand = 0
                    outputState = 3
                else:
                    theirLeftHand = 0
                    outputState = 4
            else:
                print "error Y"
        
        elif (theirLeftHand == 2 and theirRightHand == 1) or (theirLeftHand == 1 and theirRightHand == 2):
            if myLeftHand == 1 and myRightHand == 1 :
                myLeftHand = 2
                myRightHand = 0
                outputState = 5
            elif myLeftHand == 3 and myRightHand ==0:
                if theirLeftHand == 2:
                    theirLeftHand = 0
                    outputState = 1
                else:
                    theirRightHand = 0
                    outputState = 2
            elif myLeftHand == 4 and myRightHand ==0:
                myLeftHand = 2
                myRightHand = 2
                outputState = 5
            
            elif (myLeftHand == 3 and myRightHand == 2) or (myLeftHand == 2 and myRightHand == 3):
                if theirLeftHand == 2:
                    theirLeftHand == 0
                    if myLeftHand == 3:
                        outputState = 1
                    else:
                        outputState = 4
                            
                else:
                    theirRightHand = 0
                    if myLeftHand == 3:
                        outputState = 2
                    else:
                        outputState = 3 
            elif (myLeftHand == 4 and myRightHand == 2) or (myLeftHand == 2 and myRightHand == 4):
                if theirLeftHand == 2:
                    theirLeftHand = 0
                    if myLeftHand == 4:
                        outputState = 1
                    else:
                        outputState = 4
                else:
                    theirRightHand = 0
                    if myLeftHand == 4:
                        outputState = 2
                    else:
                        outputState = 3
            elif  myLeftHand == 3 and myRightHand == 3:
                if theirLeftHand == 2:
                    theirLeftHand = 0
                    outputState = 4
                else : 
                    theirRightHand = 0
                    outputState = 3
                    
                
                        
            
            else:
                print "error D"
        
        elif (theirRightHand == 4 and theirLeftHand == 0) or (theirRightHand == 0 and theirLeftHand == 4):
            if myLeftHand > 0:
                if theirRightHand == 4:
                    theirRightHand = 0
                    outputState = 2
                else: 
                     theirLeftHand = 0
                     outputState = 1
            elif myRightHand > 0:
                if theirRightHand == 4:
                    theirRightHand = 0
                    outputState = 3
                else: 
                    theirLeftHand = 0
                    outputState = 4 
            else:
                print "error ast"
                 
        elif (theirLeftHand == 1 and theirRightHand == 0) or (theirLeftHand == 0 and theirRightHand == 1):
                        
            
            if myLeftHand == 4 :
                if theirRightHand == 1:
                    outputState = 2
                    theirRightHand = 0
                else:
                    outputState = 1
                    theirLeftHand = 0
            
            elif myRightHand == 4 :
                if theirRightHand == 1:
                    outputState = 3
                    theirRightHand = 0
                else:
                    outputState = 4
                    theirLeftHand = 0            
            
            elif (myLeftHand ==2 and myRightHand ==1) or (myLeftHand ==1 and myRightHand ==2):
                myRightHand =0
                myLeftHand =3
                outputState = 5
            
                    
            elif myLeftHand == 3 and myRightHand == 3:
                myLeftHand = 4
                myRightHand = 2
                outputState = 5
            
            elif myRightHand == 2 and myLeftHand == 0:
                myLeftHand = 1
                myRightHand = 1
                outputState = 5
            elif myLeftHand == 4 and myRightHand == 3 :
                if theirLeftHand == 1:
                    theirLeftHand = 0
                    outputState = 1
                else:
                    theirRightHand = 0
                    outputState = 2
            

            else:
                print "error Q"
                
       

        elif (theirRightHand == 4 and theirLeftHand == 1) or (theirRightHand == 1 and theirLeftHand == 4):
            if (myLeftHand == 3 and myRightHand == 0) or (myLeftHand == 0 and myRightHand == 3):
                if theirRightHand == 1:
                    theirLeftHand = 0
                    if myLeftHand == 3:
                        outputState = 1
                    else:
                        outputState = 4
                else:
                    theirRightHand = 0
                    if myLeftHand == 3:
                        outputState = 2
                    else:
                        outputState = 3
            elif (myLeftHand == 4 and myRightHand ==3) or (myLeftHand == 3 and myRightHand == 4):
                theirRightHand = 0
                if myLeftHand == 4:
                    outputState = 2
                else:
                    outputState = 3
            else :
                print "error T"
                
        elif (theirRightHand ==3 and theirLeftHand == 2 )or (theirRightHand ==3 and theirLeftHand == 2 ):
            if myLeftHand == 3 and myRightHand == 3:
                if theirRightHand == 2:
                    theirRightHand = 0
                    outputState = 2
                else:
                    theirLeftHand = 0
                    outputState = 4
        
                
    
        
        return myLeftHand, myRightHand, outputState        
            