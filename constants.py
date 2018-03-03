import numpy as np

#IPs and Default Table
ServerIP = 'localhost' #the roboRIO
MainTable = "SmartDashboard" #reduces java footprint since SmartDashboard
								#is already initialized
CubeStream = 'http://localhost:5010/cam.mjpg' #axis camera stream
TapeStream = 'http://localhost:5011/cam.mjpg' #roboRIO usb stream

CubeCamera = 1
TapeCamera = 2

MaxFPS = 10

CameraPort1 = 5010
CameraPort2 = 5011

#color ranges to filter
#peg color range
cube_green_lower = np.array([26, 98, 82],np.uint8)
cube_green_upper = np.array([96, 255, 255],np.uint8)

#tower color range
tape_green_lower = np.array([72, 114, 169],np.uint8)
tape_green_upper = np.array([255, 255, 255],np.uint8)

#peg ratio values
cube_ratioMax = 9.0
cube_ratioMin = 0.0

#tower ratio values
tape_ratioMax = 0.35
tape_ratioMin = 0.18
