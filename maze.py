#code for the maze challenge

from robotFunctions import *
import newJustMid
import newJustMidMazeSide
robot.compass.Calibrate()
for i in range(20):
	print(robot.compass.Heading())

#input("Ready")
DEMO=False
exampleCode='''NextHeading = robot.compass.Heading()

def close():
	if robot.ultraFrontRight.distance()<50:
		return True
	else:
		return False

while True:
	NextHeading = (NextHeading + 90) %360
	robot.stayMid(close,45,rightSide=False,maxSpeed=1)
	robot.stop()
	time.sleep(0.1)
	robot.TurnDegreesOp3(234567890,NextHeading)'''
def run():
	sys.stderr.write("test")
	speed=0.9
	if DEMO:
		exec(exampleCode)
	else:
		def close(dist=50):
			dist1,dist2 = robot.simRead([robot.ultraFrontRight,robot.ultraFrontLeft])
			if abs(dist1-dist2)>20:
				return False
			print("mazeread",dist1,dist2)
			return (dist1+dist2)/2<dist # FIX when breadboard is finnished
		def false(dist=55):
			return False
		#FuncToStayMid = robot.stayMid2
		#FuncToStayMid = robot.mazeSection
		FuncToStayMid = robot.stayMid2
		FuncToStayMid = newJustMid.StayMid
		start = time.time()
		absHeading=robot.compass.Heading()
		while True:
			if robot.controller.B():
				break
		absHeading=robot.compass.Heading()
		heading=-90
		print("First stay mid")
		FuncToStayMid(false,20,rightSide=True,maxSpeed=speed,targetHeading=absHeading)
		print("First Turn")
		robot.stayDeg("turned",absHeading-90,absolute=True,maxSpeed=speed,params=[])
		print("Second Stay Mid")
		FuncToStayMid(false,20,rightSide=True,maxSpeed=speed,targetHeading=absHeading-90,numBefore = 8)
		print("Second Turn")
		robot.stayDeg(close,absHeading-180,absolute=True,maxSpeed=speed,params=[])
		heading=90
		print("Third turn")
		robot.stayDeg("turned",absHeading-90,absolute=True,maxSpeed=speed)
		print("Third Stay Mid")
		FuncToStayMid(false,20,rightSide=False,maxSpeed=speed,targetHeading=absHeading-90,numBefore = 1)
		print("4th start deg")
		robot.stayDeg(close,absHeading,absolute=True,maxSpeed=speed)
		heading=-90
		print("5th stayDeg")
		robot.stayDeg("turned",absHeading-90,absolute=True,maxSpeed=speed)
		print("4th stay mid")
		FuncToStayMid(false,20,rightSide=True,maxSpeed=speed,targetHeading=absHeading-90,numBefore = 3)
		print("6th stayDeg")
		robot.stayDeg("turned",absHeading-180,absolute=True,maxSpeed=speed)
		print("5th staymid")
		FuncToStayMid(false,20,StoppingDis = 60,rightSide=True,maxSpeed=speed,targetHeading=absHeading-180,numBefore = 13)
		print("7th stayDeg")
		robot.stayDeg("turned",absHeading+90,absolute=True,maxSpeed=speed)
		print("6th staymid")
		FuncToStayMid(false,20,rightSide=True,maxSpeed=speed,targetHeading=absHeading+90,numBefore=20)
		heading=90
		robot.stop()
		print(time.time()-start)
		robot.stayDeg("turned",absHeading+180,absolute=True,maxSpeed=speed)
		robot.forward(1,1)
		time.sleep(0.1)
		robot.stop()
if __name__ == "__main__":
	run()
