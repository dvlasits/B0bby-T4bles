import CalcOrder
import time
from robotFunctions import *
BlueNum = 3
YellowNum = 1
RedNum = 2
GreenNum = 4
robot.compass.Start()
input("waiting")
ops,pars = CalcOrder.listofWhat(RedNum,BlueNum,YellowNum,GreenNum)
startH = robot.compass.Heading()
for i in ops:
	if isinstance(i,int):
		robot.TurnDegreesOp3(3,startH+i)
	else:
		if len(pars[0]) == 5:
			a,b,c,d,e = pars.pop(0)
			e = (startH + e)%360
			i(a,b,c,d,e)
manual.rc()
