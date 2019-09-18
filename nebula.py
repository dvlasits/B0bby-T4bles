
#code for the nebula challenge
import CalcOrder
from robotFunctions import *
import numpy as np
import math
import pickle
import time
def run():
	robot.compass.Start()
	count = 1
	time.sleep(0.5)
	while True:
		print(robot.compass.CalibValues())
		if robot.compass.Calibrated() or count == 200:
			break
		count += 1

	robot.camera.start()
	print("Camera is Ready")
	startH = robot.compass.Heading()
	while not robot.controller.A():# or not robot.controller.connected():
		time.sleep(0.5)
	startH = robot.compass.Heading()


	def ManDis(x,y,ManDistance):
		if ManDistance:
			return abs(x[1]-y[0]) + abs(x[2] - y[1]) + abs(x[3] - y[2])
		return math.sqrt((x[1]-y[0])**2 + (x[2]-y[1])**2 + (x[3]-y[2])**2)
	def ManOrNorm(Man,Pics,cals = None):
		if Man:
			return np.argmin(np.array([ManDis(i,cals,False) for i in Pics]))
		else:
			if cals == "r":
				op1 = Pics[np.argmax(np.array([r-g-b for i,r,g,b in Pics]))]
				arr = list(Pics)
				arr[op1[0]-1] = (op1[0]-1,-100000,1000000,100000)
				op2 = arr[np.argmax(np.array([r-g-b for i,r,g,b in arr]))]
				arrayofTwo = [op1,op2]
				print("arrayofTwois")
				print(arrayofTwo)
				return arrayofTwo[np.argmin(np.array([abs(g-b) for i,r,g,b in arrayofTwo]))][0] -1
			if cals == "g":
				return np.argmax(np.array([g-b-r for i,r,g,b in Pics]))
			if cals == "b":
				return np.argmax(np.array([b-r-g for i,r,g,b in Pics]))
	#can activate with higher resolution e.g. robot.camera.start((64,64)) need to try different res's and
	#maybe no video port
	robot.TurnDegreesOp3WithJigging(45)
	pic1 = robot.camera.DanielPhoto2()
	print(robot.compass.Heading())
	time.sleep(0.2)



	robot.TurnDegreesOp3WithJigging(81,startH + 135)
	pic2 = robot.camera.DanielPhoto2()
	print(robot.compass.Heading())
	time.sleep(0.2)

	robot.TurnDegreesOp3WithJigging(81,startH + 225)
	pic3 = robot.camera.DanielPhoto2()
	print(robot.compass.Heading())
	time.sleep(0.2)

	robot.TurnDegreesOp3WithJigging(81,startH + 315)
	pic4 = robot.camera.DanielPhoto2()
	print(robot.compass.Heading())
	time.sleep(0.2)
	#f = open("ColourValues.txt", 'r')
	calibratedColours = []
	#for line in f.read().splitlines():
	#	calibratedColours.append(tuple([float(i) for i in line.split()]))
	#f.close()
	Pics = [(1,) + pic1, (2,)+pic2, (3,)+pic3, (4,)+pic4]
	UsingSquareSum = False #False for cam classify
	calibratedColours = ["r","g","b"] #Add this line for camclassify
	WhichRed = ManOrNorm(UsingSquareSum,Pics,calibratedColours[0])
	print(Pics[WhichRed])
	RedNum = Pics[WhichRed][0]
	Pics.pop(WhichRed)
	WhichGreen = ManOrNorm(UsingSquareSum,Pics,calibratedColours[1])
	print(Pics[WhichGreen])
	GreenNum = Pics[WhichGreen][0]
	Pics.pop(WhichGreen)
	WhichBlue = ManOrNorm(UsingSquareSum,Pics,calibratedColours[2])
	print(Pics[WhichBlue])
	BlueNum = Pics[WhichBlue][0]
	Pics.pop(WhichBlue)
	YellowNum = Pics[0][0]
	print(Pics[0])
	print("Red pos is {} Blue pos is {} Green pos is {} Yellow pos is {}".format(RedNum,BlueNum,GreenNum,YellowNum))
	#YellowNum = np.argmax(np.array([r1+g1-4*b1,r2+g2-4*b2,r3+g3-4*b3,r4+g4-4*b4]))'''

	ops,pars = CalcOrder.listofWhat(RedNum,BlueNum,YellowNum,GreenNum,IsAngle = True)
	print(ops,pars)
	startH = robot.compass.Heading()
	overalreadings,overallspeeds = [],[]
	start = time.time()
	for i in ops:
		if isinstance(i,int):
			robot.TurnDegreesOp3(3,startH+i+45)
		else:
			if len(pars[0]) == 5:
				a,b,c,d,e = pars.pop(0)
				e = (startH + 45 + e)%360
				if i == robot.stop5Forwards:
					readings,speeds = i(a,b,c,d,e)
					overallspeeds.append(speeds)
					overalreadings.append(readings)
					#plt.scatter(readings,speeds)
				else:
					i(a,b,c,d,e)
				ForOrBack = d
			else:
				raise RuntimeError("Too many parameters input")
	if d:
		robot.forward(-1,-1)
	else:
		robot.forward(1,1)
	time.sleep(0.2)
	robot.stop()
	print(time.time()-start)
	with open("overallspeeds.txt","wb") as fp:
		pickle.dump(overallspeeds, fp)
	with open("overalreadings.txt","wb") as fp:
		pickle.dump(overalreadings, fp)
	print("saved to file")
	'''for index1,index2 in zip(overalreadings,overallspeeds):
		plt.scatter(index1,index2)
	plt.show()'''
	manual.rc()
	while not robot.controller.A():# or not robot.controller.connected():
		time.sleep(0.5)


	ops,pars = CalcOrder.listofWhat(RedNum,BlueNum,YellowNum,GreenNum)
	startH = robot.compass.Heading()
	overalreadings,overallspeeds = [],[]
	start = time.time()
	for i in ops:
		if isinstance(i,int):
			robot.TurnDegreesOp3(3,startH+i)
		else:
			if len(pars[0]) == 5:
				a,b,c,d,e = pars.pop(0)
				e = (startH + e)%360
				if i == robot.stop5Forwards:
					readings,speeds = i(a,b,c,d,e)
					overallspeeds.append(speeds)
					overalreadings.append(readings)
					#plt.scatter(readings,speeds)
				else:
					i(a,b,c,d,e)
				ForOrBack = d
			else:
				raise RuntimeError("Too many parameters input")
	if d:
		robot.forward(-1,-1)
	else:
		robot.forward(1,1)
	time.sleep(0.2)
	robot.stop()
	print(time.time()-start)
	with open("overallspeeds.txt","wb") as fp:
		pickle.dump(overallspeeds, fp)
	with open("overalreadings.txt","wb") as fp:
		pickle.dump(overalreadings, fp)
	'''for index1,index2 in zip(overalreadings,overallspeeds):
		plt.scatter(index1,index2)
	plt.show()'''
	manual.rc()

	while not robot.controller.A():# or not robot.controller.connected():
		time.sleep(0.5)
	startTime = time.time()

	ops,pars = CalcOrder.listofWhat(RedNum,BlueNum,YellowNum,GreenNum)
	startH = robot.compass.Heading()
	overalreadings,overallspeeds = [],[]
	start = time.time()
	for i in ops:
		if isinstance(i,int):
			robot.TurnDegreesOp3(3,startH+i)
		else:
			if len(pars[0]) == 5:
				a,b,c,d,e = pars.pop(0)
				e = (startH + e)%360
				if i == robot.stop5Forwards:
					readings,speeds = i(a,b,c,d,e)
					overallspeeds.append(speeds)
					overalreadings.append(readings)
					#plt.scatter(readings,speeds)
				else:
					i(a,b,c,d,e)
				ForOrBack = d
			else:
				raise RuntimeError("Too many parameters input")
	if d:
		robot.forward(-1,-1)
	else:
		robot.forward(1,1)
	time.sleep(0.2)
	robot.stop()
	print(time.time()-start)
	with open("overallspeeds.txt","wb") as fp:
		pickle.dump(overallspeeds, fp)
	with open("overalreadings.txt","wb") as fp:
		pickle.dump(overalreadings, fp)
	'''for index1,index2 in zip(overalreadings,overallspeeds):
		plt.scatter(index1,index2)
	plt.show()'''
if __name__=="__main__":
	run()
