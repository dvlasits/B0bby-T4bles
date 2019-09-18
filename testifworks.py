from robotFunctions import *
robot.forward(0.3,0.3)
while robot.ultraFrontLeftSide.distance() < 50:
	pass
robot.stop()
