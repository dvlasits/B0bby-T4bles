from robotFunctions import *

def StayCourse(Speed = 1, StartSpeed = 1, Heading = robot.compass.Heading(), DisToStop = 50, Timed = False, TimeToStop = 4):
    StartTime = time.time()
    while robot.ultraFrontRight.distance() > DisToStop and not Timed or Timed and time.time() > StartTime + TimeToStop:

        direction = robot.WhichWay(Heading,robot.compass.Heading())
        if direction > 2:
            if StartSpeed > 0:
                robot.forward(StartSpeed*robot.AmountToReduce(abs(direction)),StartSpeed)
            else:
                robot.forward(StartSpeed,StartSpeed*robot.AmountToReduce(abs(direction)))
        elif direction < -2:
            if StartSpeed > 0:
                robot.forward(StartSpeed,StartSpeed*robot.AmountToReduce(abs(direction)))
            else:
                robot.forward(StartSpeed*robot.AmountToReduce(abs(direction)),StartSpeed)
        else:
            robot.forward(StartSpeed,StartSpeed)




def StayMid(Speed = 1,Heading = robot.compass.Heading(),rightSide=True,DisToBe=22,threshold=4,DisToStop = 30, Ultra = robot.ultraFrontRightSide):

    def DisToWall(rightSide):
    	if rightSide:
    		F,B = robot.simRead([robot.ultraFrontRightSide, robot.ultraBackRightSide])
    		return (F+B)/2
    	F,B = robot.simRead([robot.ultraFrontLeftSide,robot.ultraBackLeftSide])
    	return (F+B)/2

	'''if abs(robot.WhichWay(Heading,robot.compass.Heading())) > 30:
		print("Activated get straight code")
		robot.stayDeg("turned",Heading,absolute=False,MaxSpeed=Speed)'''
	while Ultra.distance() < DisToStop:
		DisToWallNow = DisToWall(rightSide)
		angle = ((DisToWallNow-5)/(39-5))*(20--20) + - 20
		HeadingNeeded = (Heading + angle)%360
		direction = robot.WhichWay(HeadingNeeded,robot.compass.Heading())
		#print(direction)
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


input("Waiting to go")


FuncToStayMid = StayMid
DisToStop = 30


TurnOrder = [(True, -45,robot.ultraFrontLeftSide),(True, 45,robot.ultraFrontRightSide),(False, 45,robot.ultraFrontRightSide),(False,-45,robot.ultraFrontLeftSide),(True,0,robot.ultraFrontRight)]
Heading = robot.compass.Heading()
for i in range(5):
        FuncToStayMid(Heading = Heading, DisToStop = DisToStop,rightSide = TurnOrder[0][0],Ultra = TurnOrder[i][2])
        Heading = (Heading + TurnOrder[0][1]) % 360
        robot.stayDeg("turned",deg = Heading)
robot.stop()
