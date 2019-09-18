#code for the maze challenge

from robotFunctions import *
import newJustMid
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
		def close(dist=55):
			distRead = robot.ultraFrontRight.distance()
			print("mazeread"+str(distRead))
			return distRead<dist # FIX when breadboard is finnished
		def false(dist=55):
			return False
		#FuncToStayMid = robot.stayMid2
		#FuncToStayMid = robot.mazeSection
		FuncToStayMid = robot.stayMid2
		FuncToStayMid = newJustMid.StayMid
		start = time.time()
		absHeading=robot.compass.Heading()
		time.sleep(1)
		absHeading=robot.compass.Heading()
		heading=90
		for i in range(10):
			print("First stay mid")
			FuncToStayMid(false,20,rightSide=False,maxSpeed=speed,targetHeading=absHeading)
			print("First Turn")
			robot.stayDeg("turned",heading,absolute=False,maxSpeed=speed,params=[])
			print("Second Stay Mid")
			absHeading  = (absHeading + 90)%360

		robot.stop()
		print(time.time()-start)
		#robot.stayDeg("turned",heading,absolute=False,maxSpeed=speed)

if __name__ == "__main__":
	run()
