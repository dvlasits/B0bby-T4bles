#code for the speed test challenge:
from robotFunctions import *
import time
import newJustMidMaze
#0x3F set to 20
#time.sleep(2)
#see if it reading
robot.compass.Calibrate()
def run():
	def bend():
		if robot.ultraFrontLeftSide.distance() > 50 or robot.ultraFrontRightSide.distance() > 50:
			return True
		else:
			return False
	def false():
		return time.time()-start>0.9
	def go():
		global start
		robot.stayMid(bend,15,maxSpeed=1)
		start=time.time()+0.3
		robot.stayDeg(false,-30,maxSpeed=1)
		start=time.time()-0.3
		robot.stayMid(false,40)
		start=time.time()+0.15
		robot.stayDeg(false,35)
		start=time.time()-0.3
		robot.stayDeg(false,-35)
		robot.stayMid(bend,20)
	def go2():
		speed=0.85
		a=robot.compass.Heading()
		time.sleep(0.5)
		a=robot.compass.Heading()
		robot.stayMid2(bend,20,maxSpeed=speed,rightSide=True)
		robot.stayDeg("turned",45,maxSpeed=speed)
		robot.stayMid2(bend,20,maxSpeed=speed,rightSide=False)
		robot.stayDeg("turned",-45,maxSpeed=speed)
		robot.stayMid2(bend,20,maxSpeed=speed,rightSide=False)
		robot.stayDeg("turned",-45,maxSpeed=speed)
		robot.stayMid2(bend,20,maxSpeed=speed,rightSide=True)
		robot.stayDeg("turned",45,maxSpeed=speed)
		robot.stayMid2(bend,20,maxSpeed=speed,rightSide=True)
	def go3():
		speed1=1
		speed2=0.8
		a=robot.compass.Heading()
		time.sleep(0.5)
		a=robot.compass.Heading()
		newJustMidMaze.StayMid(bend,30,maxSpeed=speed1,rightSide=True, targetHeading = a,DisToBe = 27)
		robot.stayDeg("turned",a-45,absolute=True,maxSpeed=speed2)
		newJustMidMaze.StayMid(bend,20,maxSpeed=speed1,rightSide=True, targetHeading = (a - 45)%360)
		robot.stayDeg("turned",a,absolute=True,maxSpeed=speed2)
		newJustMidMaze.StayMid(bend,20,maxSpeed=speed1,rightSide=False, targetHeading = a,DisToBe = 30)
		robot.stayDeg("turned",a+45,absolute=True,maxSpeed=speed2)
		newJustMidMaze.StayMid(bend,20,maxSpeed=speed1,rightSide=False, targetHeading = (a+45)%360)
		robot.stayDeg("turned",a,absolute=True,maxSpeed=speed2)
		startTime=time.time()
		def timeDelta():
			if time.time()-startTime>0.5:
				return True
			return False
		#robot.stayDeg(timeDelta,a+7,absolute=True,maxSpeed=speed1)
		newJustMidMaze.StayMid(bend,20,maxSpeed=speed1,rightSide=True, targetHeading = a,DisToBe = 18)
		
	go3()
if __name__=="__main__":
	input("ready?")
	run()
