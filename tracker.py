import numpy as np
import cv2
import logging
import constants
import imutils
import math
from networktables import NetworkTables

logging.basicConfig(level=logging.DEBUG)
NetworkTables.initialize(server=constants.ServerIP)
Table = NetworkTables.getTable(constants.MainTable)

camera = cv2.VideoCapture(constants.CubeStream)

def trackCube():
    while(True):
        (grabbed, frame) = camera.read()
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #sharpen and refine image
        hsv = cv2.GaussianBlur(hsv, (7, 7), 0)
        hsv = cv2.erode(hsv, None, iterations=2)
        hsv = cv2.dilate(hsv, None, iterations=2)

        #filter anything based on color
        green_range = cv2.inRange(hsv, constants.cube_green_lower, constants.cube_green_upper)
        
        areaArray = []
        
        #will error if unable to get camera feed
        try:
            b, contours, _ = cv2.findContours(green_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours: 
            
                #ignore all small contours
                if cv2.contourArea(c) < 5000:
                    Table.putBoolean("ContoursFound", False)
                    continue 
                    
                #first sort the array by area
                sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
            
                #find biggest contour, mark it
                if len(contours)>0:
                     green=max(contours, key=cv2.contourArea)
                     (xg,yg,wg,hg) = cv2.boundingRect(green)
                     
                     #draw the rectangle to screen
                     axOne = cv2.rectangle(frame, (xg,yg), (xg+wg, yg+hg), (0,255,0), 2)
                
                CubeData = [xg, yg, wg, hg]
                CenterOfCube = xg+(wg/2)
                
                ImageSizeInDeg = CenterOfCube * constants.DegPerPixel
                
                DistanceToCube = ((13/math.tan(math.radians(ImageSizeInDeg))))
                
                PixelsToCube = CenterOfCube - 300
                
                AngleToCube = ((CenterOfCube - (constants.CameraWidth/2)) * constants.DegPerPixel)
                
                #send data to table
                Table.putNumber("DistanceToCube", DistanceToCube)
                Table.putNumber("PixelsToCube", PixelsToCube)
                Table.putNumberArray("X, Y, W, H", CubeData)
                Table.putNumber("CenterOfCube", CenterOfCube)
                Table.putNumber("AngleToCube", AngleToCube)
                Table.putBoolean("ContoursFound", True)

        except IndexError:
            Table.putBoolean("ContoursFound", False)

        cv2.imshow("Frame", frame)
        cv2.imshow("Frame", frame) #enable for debug
        key = cv2.waitKey(1) & 0xFF
        
        if key ==ord("q"):
            break
