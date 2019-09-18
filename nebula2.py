
#code for the nebula challenge
from robotFunctions import *
import numpy as np
import math
import time
robot.compass.Start()
count = 1
while True:
	print(robot.compass.CalibValues())
	if robot.compass.Calibrated() or count == 200:
		break
	count += 1
input("done")
startH = robot.compass.Heading()
print(startH)

def ManDis(x,y,ManDistance):
	if ManDistance:
		return abs(x[1]-y[0]) + abs(x[2] - y[1]) + abs(x[3] - y[2])
	return math.sqrt((x[1]-y[0])**2 + (x[2]-y[1])**2 + (x[3]-y[2])**2)
def ManOrNorm(Man,Pics,cals = None):
	if Man:
		return np.argmin(np.array([ManDis(i,cals,False) for i in Pics]))
	else:
		if cals == "r":
			return np.argmax(np.array([r-g-b for i,r,g,b in Pics]))
		if cals == "g":
			return np.argmax(np.array([g-b-r for i,r,g,b in Pics]))
		if cals == "b":
			return np.argmax(np.array([b-r-g for i,r,g,b in Pics]))
robot.camera.start() #can activate with higher resolution e.g. robot.camera.start((64,64)) need to try different res's and
#maybe no video port
robot.TurnDegreesOp3(45)
pic1 = robot.camera.DanielPhoto2()
print(robot.compass.Heading())
time.sleep(0.2)



robot.TurnDegreesOp3(81,startH + 135)
pic2 = robot.camera.DanielPhoto2()
print(robot.compass.Heading())
time.sleep(0.2)

robot.TurnDegreesOp3(81,startH + 225)
pic3 = robot.camera.DanielPhoto2()
print(robot.compass.Heading())
time.sleep(0.2)

robot.TurnDegreesOp3(81,startH + 315)
pic4 = robot.camera.DanielPhoto2()
print(robot.compass.Heading())

f = open("ColourValues.txt", 'r')
calibratedColours = []
for line in f.read().splitlines():
	calibratedColours.append(tuple([float(i) for i in line.split()]))
f.close()
Pics = [(1,) + pic1, (2,)+pic2, (3,)+pic3, (4,)+pic4]
UsingSquareSum = False #False for cam classify
calibratedColours = ["r","g","b"] #Add this line for camclassify
WhichRed = ManOrNorm(UsingSquareSum,Pics,calibratedColours[0])
print(Pics[WhichRed])
RedNum = Pics[WhichRed][0]
Pics.pop(WhichRed)
WhichGreen = ManOrNorm(UsingSquareSum,Pics,calibratedColours[1])
print(Pics[WhichGreen])
GreenNum = Pics[WhichGreen][0]
Pics.pop(WhichGreen)
WhichBlue = ManOrNorm(UsingSquareSum,Pics,calibratedColours[2])
print(Pics[WhichBlue])
BlueNum = Pics[WhichBlue][0]
Pics.pop(WhichBlue)
YellowNum = Pics[0][0]
print(Pics[0])
print("Red pos is {} Blue pos is {} Green pos is {} Yellow pos is {}".format(RedNum,BlueNum,GreenNum,YellowNum))
#YellowNum = np.argmax(np.array([r1+g1-4*b1,r2+g2-4*b2,r3+g3-4*b3,r4+g4-4*b4]))'''

def ForWardsAndBack(GoBack):
	robot.stop5(33,-0.3,12,1,GoBack,False)
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
