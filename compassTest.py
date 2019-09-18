from robotFunctions import *
import time
while True:
	mx=0
	for i in range(100):
		startTime=time.time()
		heading,dist=robot.compass.Heading(),robot.ultraFrontRight.distance()
		endTime=time.time()
		timeDelta=endTime-startTime
		mx=max(mx,timeDelta)
		if timeDelta>0.05:
			print(timeDelta)
			quit()
	print(timeDelta,mx,heading)
