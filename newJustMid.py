from robotFunctions import *
def DisToWall(rightSide):
	if rightSide:
		F,B = robot.simRead([robot.ultraFrontRightSide, robot.ultraBackRightSide])
		return (F+B)/2,1
	F,B = robot.simRead([robot.ultraFrontLeftSide,robot.ultraBackLeftSide])
	return (F+B)/2,1

def AmountToReduce(absDirection):
	speedMin = 0
	AngleMax = 10
	if absDirection > AngleMax:
		return speedMin
	return 1-((((absDirection-2)/(AngleMax-2))*(1-speedMin)) + speedMin)


def StayMid(useless1, useless2, maxSpeed = 1,targetHeading = robot.compass.Heading(),rightSide=True,DisToBe=15,threshold=4,useUltras = True,StoppingDis = 55,numBefore = 15):


	#if abs(robot.WhichWay(Heading,robot.compass.Heading())) > 30:
	#rint("Activated get straight code")
	#robot.stayDeg("turned",Heading,absolute=False,MaxSpeed=Speed)
	#if abs(DisToBe - DisToWall(rightSide)) < threshold:
	#robot.stayDeg(TimeToGoBackToMiddle,Heading,True,Speed)
	Heading = targetHeading
	Speed = maxSpeed
	count = 0
	while True:
		count += 1
		if useUltras:
			DisToWallNow,RFront = DisToWall(rightSide)
			#print(RFront)
			#print(DisToWallNow)
			angle = ((DisToWallNow-(DisToBe-40))/((DisToBe+40)-(DisToBe-40)))*(40--40) + - 40
			if rightSide:
				HeadingNeeded = (Heading + angle)%360
			else:
				HeadingNeeded = (Heading - angle)%360
			direction = robot.WhichWay(HeadingNeeded, robot.compass.Heading())
		else:
			RFront = robot.ultraFrontRight.distance()
			direction = robot.WhichWay(Heading,robot.compass.Heading())
		#rint(direction)
		if direction > 2:
			if Speed > 0:
				robot.forward(Speed*AmountToReduce(abs(direction)),Speed)
			else:
				robot.forward(Speed,Speed*AmountToReduce(abs(direction)))
		elif direction < -2:
			if Speed > 0:
				robot.forward(Speed,Speed*AmountToReduce(abs(direction)))
			else:
				robot.forward(Speed*AmountToReduce(abs(direction)),Speed)
		else:
			robot.forward(Speed,Speed)
		dis1,dis2 = robot.simRead([robot.ultraFrontRight,robot.ultraFrontLeft])
		print(dis1,dis2)
		if abs(1-dis1/dis2)<0.2:
			if (dis1+dis2)/2 < StoppingDis and count > numBefore:
				break
