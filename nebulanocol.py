from robotFunctions import *
import manual
manual.rc()
count = 0
while True:
	print(robot.compass.CalibValues())
	if robot.compass.Calibrated() or count == 200:
		break
	count += 1
input("done")
RedNum = 1
GreenNum = 2
YellowNum = 3
BlueNum = 4
startH = robot.compass.Heading()
def ForWardsAndBack(GoBack,whichUltra):
	robot.stop5Forwards(33,-0.3,12,whichUltra)
	if GoBack:
		robot.back5(22,0.1,55,whichUltra)
	else:
		robot.stop()

HowMuchToTurn = (startH + 45 + ((RedNum-1)*-90))
robot.TurnDegreesOp2(2,HowMuchToTurn)
ForWardsAndBack(True)
HowMuchToTurn = (startH + 45 + ((BlueNum-1)*-90))
robot.TurnDegreesOp2(2,HowMuchToTurn)
ForWardsAndBack(True)
HowMuchToTurn = (startH + 45 + ((YellowNum-1)*-90))
robot.TurnDegreesOp2(2,HowMuchToTurn)
ForWardsAndBack(True)
HowMuchToTurn = (startH + 45 + ((GreenNum-1)*-90))
robot.TurnDegreesOp2(2,HowMuchToTurn)
'''robot.forward(0.4,0.4)
while robot.ultraFrontLeft.distance() > 13 and not robot.controller.A():
	pass
robot.stop()'''
ForWardsAndBack(False)
from manual import *
