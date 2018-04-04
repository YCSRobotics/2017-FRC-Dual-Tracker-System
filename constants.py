import numpy as np

#IPs and Default Table
ServerIP = "localhost" #the roboRIO
MainTable = "SmartDashboard" #reduces java footprint since SmartDashboard
								#is already initialized
CubeStream = 0 #Bottom Camera
TapeStream = 'http://localhost:1182/stream.mjpg' #Top Camera

CubeCamera = 1
TapeCamera = 2

MaxFPS = 8

CameraWidth = 600
FieldOfView = 60
DegPerPixel = FieldOfView/CameraWidth

#color ranges to filter
#peg color range
cube_green_lower = np.array([24, 59, 134],np.uint8)
cube_green_upper = np.array([73, 243, 255],np.uint8)

#tower color range
tape_green_lower = np.array([72, 114, 169],np.uint8)
tape_green_upper = np.array([255, 255, 255],np.uint8)

#peg ratio values
cube_ratioMax = 1.5
cube_ratioMin = 1.0

#tower ratio values
tape_ratioMax = 0.35
tape_ratioMin = 0.18
