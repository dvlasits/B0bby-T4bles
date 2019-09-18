#Dan Maze

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




def StayMid(useless1, useless2,maxSpeed = 1,targetHeading = robot.compass.Heading(),rightSide=True,DisToStop = 50,DisToBe=22,threshold=4):
    Heading = targetHeading
    Speed = maxSpeed
    def DisToWall(rightSide):
        if rightSide:
            F,B = robot.simRead([robot.ultraFrontRightSide, robot.ultraBackRightSide])
            return (F+B)/2
        F,B = robot.simRead([robot.ultraFrontLeftSide,robot.ultraBackLeftSide])
        return (F+B)/2


    while robot.ultraFrontRight.distance() > DisToStop:
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
DisToStop = 40


TurnOrder = [(FuncToStayMid,-90),(FuncToStayMid,-90),(StayCourse,90),(FuncToStayMid,90),(StayCourse,-90),(FuncToStayMid,-90),(FuncToStayMid,-90),(FuncToStayMid,90)]
Heading = robot.compass.Heading()
for i in range(9):
        if i != 3 and i != 7 and i != 8:
            TurnOrder[i][0](Heading = Heading, DisToStop = DisToStop)
        elif i == 3:
            TurnOrder[i][0](Heading = Heading,rightSide = False, DisToStop = DisToStop)

        elif i == 7:
            TurnOrder[i][0](Heading = Heading, DisToStop = 100)
            StayCourse(Heading = Heading, DisToStop = DisToStop)
        elif i == 8:
            robot.stop()
            break
            StayCourse(Heading = Heading, Timed = True, TimeToStop = 5)
            robot.stop()
            break


        robot.stop()
        time.sleep(0.1)
        Heading = (Heading + TurnOrder[i][1]) % 360
        robot.TurnDegreesOp3(1234567890,Heading)



'''if abs(robot.WhichWay(Heading,robot.compass.Heading())) > 30:
    print("Activated get straight code")
    robot.stayDeg("turned",Heading,absolute=False,MaxSpeed=Speed)'''
