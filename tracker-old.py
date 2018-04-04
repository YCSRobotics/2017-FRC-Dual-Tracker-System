import numpy as np
import cv2
import logging
import constants
import math
from networktables import NetworkTables
from imutils.video import WebcamVideoStream

#NOTES:
#TEST IF MAIN ROBOT.PY CAN SET THE NETWORKTABLE INFORMATION
#IF SO STATEMACHINE IS A SUCCESS
logging.basicConfig(level=logging.DEBUG)

#grab frames using multithreading
#and initialize the camera
vs0 = cv2.VideoCapture(1)
vs1 = cv2.VideoCapture(constants.TapeStream)

NetworkTables.initialize(server=constants.ServerIP)
Table = NetworkTables.getTable(constants.MainTable)
    
def trackCube():
    while (True):

        if(Table.getNumber("PiState", 0) != 0):
            break
        else:
            pass

        #grab current frame from multithreaded process
        ret, frame0 = vs0.read()
        hsv = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)

        #create the range of colour min/max
        green_range = cv2.inRange(hsv, constants.cube_green_lower, constants.cube_green_upper)

        #create blank area for sort
        areaArray = []
        print("Tracking Robot")
        try:
            #grab all contours based on colour range
            b, contours, _ = cv2.findContours(green_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     
            if len(contours) > 0: 
        
                 #find biggest contour, mark it
                 green=max(contours, key=cv2.contourArea)
                 (x,y,w,h) = cv2.boundingRect(green)
                 
                 #find aspect ratio of contour
                 aspect_ratio1 = float(w)/h
				 
                 #put aspect ratio for debug
                 Table.putNumber("CubeAspectRation", aspect_ratio1)
                 
                 #only run if contour is within ratioValues
                 if aspect_ratio1 <= constants.cube_ratioMax and aspect_ratio1 >= constants.cube_ratioMin:

                     #make the largest values always right rect
                     #this prevents negative values when not wanted
                     Values = [x, y, w, h]
                     TargetWidth = (x+w)
                     CenterOfTarget = TargetWidth/2

                     GetImageSizeInDeg = constants.DegPerPixel * TargetWidth
                     
                     AngleToCube = ((CenterOfTarget - (constants.CameraWidth/2)) * constants.DegPerPixel)
                     
                     #put values to networktable
                     Table.putNumber("AngleToCube", AngleToCube)
                     Table.putNumber("CubeWidth", TargetWidth)
                     Table.putNumberArray("Values", Values)
                     Table.putNumber("CubeCenterOfTarget", CenterOfTarget)
                     Table.putBoolean("CubeNoContoursFound", False)
                     
                 else: #contour not in aspect ratio
                     Table.putBoolean("CubeNoContoursFound", True)

        except IndexError: #no contours found
            Table.putBoolean("CubeNoContoursFound", True)
            
def trackTape():
    while (True):
    
        k = cv2.waitKey(1) & 0xFF
        # press 'q' to exit
        if k == ord('q'):
            break

        if(Table.getNumber("PiState", 0) != 0):
            break
        else:
            pass

        #grab current frame from multithreaded process
        frame0 = vs0.read()
        
        #convert to HSV
        hsv = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)

        #create the range of colour min/max
        green_range = cv2.inRange(hsv, constants.tape_green_lower, constants.tape_green_upper)

        #create blank area for sort
        areaArray = []
        try:
            #grab all contours based on colour range
            b, contours, _ = cv2.findContours(green_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #order contours into an array by area
            for i, c in enumerate(contours):
                area = cv2.contourArea(c)
                areaArray.append(area)
            
            #sort the array by greatest to smallest
            sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
            
            #find the nth largest contour [n-1][1], in this case 2
            secondlargestcontour = sorteddata[1][1]
            
            if len(contours) > 0: 
            #draw it #find second biggest contour, mark it.
                 x, y, h, w = cv2.boundingRect(secondlargestcontour)
                 cv2.drawContours(frame0, secondlargestcontour, -1, (0, 0, 255), 0)
        
                 #find biggest contour, mark it
                 green=max(contours, key=cv2.contourArea)
                 (xg,yg,wg,hg) = cv2.boundingRect(green)
                 
                 #find aspect ratio of contour
                 aspect_ratio1 = float(wg)/hg
                 aspect_ratio2 = float(w)/h

                 Table.putNumber("TapeAspectRatio1", aspect_ratio1)
                 Table.putNumber("TapeAspectRatio2", aspect_ratio2)
                 
                 #only run if contour is within ratioValues
                 if (aspect_ratio1 and aspect_ratio2 <= constants.tape_ratioMax 
				 and aspect_ratio1 and aspect_ratio2 >= constants.tape_ratioMin):

                     #make the largest values always right rect
                     #this prevents negative values when not wanted
                     if (xg+wg) > x:
                        CenterOfTarget = (xg+wg-x)/2
                     else:
                        CenterOfTarget = (x-xg+wg)/2

                     if x < (xg+w):
                        TapeWidth = (x+CenterOfTarget)
                     else:
                        TapeWidth = (xg+w+CenterOfTarget)

                     #put values to networktable
                     Table.putNumber("TapeWidth", TapeWidth)
                     Table.putNumber("TapeCenterOfTarget", CenterOfTarget)
                     Table.putBoolean("TapeNoContoursFound", False)
                     
                 else: #contour not in aspect ratio
                     Table.putBoolean("TapeNoContoursFound", True)

        except IndexError: #no contours found
            Table.putBoolean("TapeNoContoursFound", True)


def piState():
    return Table.getNumber("PiState", 0)

#roboRIO streams camera USB servers on ports 1181+
#Example- 10.0.66.2:1181

