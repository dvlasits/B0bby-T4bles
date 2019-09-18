from robotFunctions import *
time.sleep(0.5)
robot.forward(1,1)
time.sleep(0.3)
robot.forward(0.7,0.7)
while not robot.controller.A():
	pass
robot.stop()
from manual import *
