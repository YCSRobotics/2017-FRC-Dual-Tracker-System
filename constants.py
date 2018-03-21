import numpy as np

#IPs and Default Table
ServerIP = '10.0.66.2' #the roboRIO
MainTable = "SmartDashboard" #reduces java footprint since SmartDashboard
								#is already initialized
CubeStream = 'http://localhost:1181/stream.mjpg' #Bottom Camera
TapeStream = 'http://localhost:1182/stream.mjpg' #Top Camera

CubeCamera = 1
TapeCamera = 2

MaxFPS = 8

CameraWidth = 320
CameraHeight = 240

#color ranges to filter
#peg color range
cube_green_lower = np.array([26, 98, 82],np.uint8)
cube_green_upper = np.array([96, 255, 255],np.uint8)

#tower color range
tape_green_lower = np.array([72, 114, 169],np.uint8)
tape_green_upper = np.array([255, 255, 255],np.uint8)

#peg ratio values
cube_ratioMax = 1.5
cube_ratioMin = 1.0

#tower ratio values
tape_ratioMax = 0.35
tape_ratioMin = 0.18
