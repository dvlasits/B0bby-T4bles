from robotFunctions import *
import time
start = time.time()
for i in range(10):
	robot.ultraFrontLeft.distance()
print(time.time()-start)
