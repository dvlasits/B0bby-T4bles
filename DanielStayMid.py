from robotFunctions import *
def DisToWall(rightSide):
	if rightSide:
		F,B,RFront = robot.simRead([robot.ultraFrontRightSide, robot.ultraBackRightSide,robot.ultraFrontRight])
		return (F+B)/2,RFront
	F,B,RFront = robot.simRead([robot.ultraFrontLeftSide,robot.ultraBackLeftSide,robot.ultraFrontRight])
	return (F+B)/2,RFront


def StayMid(Speed = 1,Heading = robot.compass.Heading(),rightSide=True,DisToBe=22,threshold=4,useUltras = True,StoppingDis = 47):
	#input("Waiting")
	#if abs(robot.WhichWay(Heading,robot.compass.Heading())) > 30:
	#rint("Activated get straight code")
	#robot.stayDeg("turned",Heading,absolute=False,MaxSpeed=Speed)
	#if abs(DisToBe - DisToWall(rightSide)) < threshold:
	#robot.stayDeg(TimeToGoBackToMiddle,Heading,True,Speed)
	while True:
		if useUltras:
			DisToWallNow,RFront = DisToWall(rightSide)

			angle = ((DisToWallNow-5)/(39-5))*(20--20) + - 20
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
				robot.forward(Speed*robot.AmountToReduce(abs(direction)),Speed)
			else:
				robot.forward(Speed,Speed*robot.AmountToReduce(abs(direction)))
		elif direction < -2:
			if Speed > 0:
				robot.forward(Speed,Speed*robot.AmountToReduce(abs(direction)))
			else:
				robot.forward(Speed*robot.AmountToReduce(abs(direction)),Speed)
		else:
			robot.forward(Speed,Speed)
		print(RFront)
		if RFront < StoppingDis:
			robot.stop()
			break
robot.compass.Calibrate()
input("ready")
startTime = time.time()
TurnFunc = robot.TurnDegreesOp3
sleepingTime = 0.1
sleepingTimeAfterTurning = 0.1
StartHeading = robot.compass.Heading()
StayMid(Heading = StartHeading)
time.sleep(sleepingTime)
TurnFunc(123456789,(StartHeading -90)%360)
time.sleep(sleepingTimeAfterTurning)
StayMid(Heading = (StartHeading -90)%360)
time.sleep(sleepingTime)
TurnFunc(1234567,(StartHeading - 180)% 360)
time.sleep(sleepingTimeAfterTurning)
StayMid(Heading = (StartHeading - 180)% 360,useUltras = False,StoppingDis = 40)
time.sleep(sleepingTime)
TurnFunc(1234567,(StartHeading -90)%360)
time.sleep(sleepingTimeAfterTurning)
StayMid(Heading = (StartHeading -90)%360, rightSide = False,StoppingDis = 40)
time.sleep(sleepingTime)
TurnFunc(123456789,StartHeading)
time.sleep(sleepingTimeAfterTurning)
StayMid(Heading = StartHeading, useUltras = False,StoppingDis = 40)
time.sleep(sleepingTime)
TurnFunc(123456789,(StartHeading -90)%360)
time.sleep(sleepingTimeAfterTurning)
StayMid(Heading = (StartHeading -90)%360,StoppingDis = 40)
time.sleep(sleepingTime)
TurnFunc(12345678,(StartHeading - 180)%360)
time.sleep(sleepingTimeAfterTurning)
StayMid(Heading = (StartHeading - 180)%360)
time.sleep(sleepingTime)
TurnFunc(123456789,(StartHeading + 90)%360)
time.sleep(sleepingTimeAfterTurning)
StayMid(Heading = (StartHeading + 90)%360)
print("timeTaken")
print(time.time()-startTime)
