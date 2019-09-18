#SetupSensors
from random import randint
import RPi.GPIO as GPIO
import ThunderBorg3
import time
GPIO.setmode(GPIO.BCM)
import xbox
import logging
import sys
from Adafruit_BNO055 import BNO055
import io
import picamera
from PIL import Image
import numpy as np
import atexit
import math
import matplotlib.pyplot as plt
import pickle

#[216, 255, 185, 255, 217, 255, 206, 7, 140, 252, 15, 241, 254, 255, 255, 255, 255, 255, 232, 3, 10, 3]
class Compass:
	def __init__(self):
		self.started = False
	def Start(self):
		if not self.started:
			operational = False
			self.bno = BNO055.BNO055(serial_port='/dev/serial0')
			for i in range(10):
				try:
					if not self.bno.begin():
						raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
					else:
						operational = True
						break
				except RuntimeError:
					pass
			if not operational:
				raise RuntimeError('Cant connect to compass after 10 attempts')
			self.SetValues([240, 255, 216, 255, 240, 255, 222, 246, 167, 3, 91, 241, 254, 255, 254, 255, 255, 255, 232, 3, 225, 2])
			print("Making sure not reading 0 heading")
			while True:

				if self.Heading() != 0:
					break
				print("You need to shake to stop heading being 0")
			print("now safe to put down")
			self.started = True
	def Calibrate(self):
		for i in range(50):
			print(self.CalibValues())
			time.sleep(0.2)

	def ShowLED(self):
		sys, gyro, accel, mag = self.CalibValues
		if sys == 3:
			robot.controller.TopRightOn()
		else:
			robot.controller.TopRightOff()
		if gyro == 3:
			robot.controller.BottomLeftOn()
		else:
			robot.controller.BottomeLeftOff()
		if accel == 3:
			robot.controller.BottomRightOn()
		else:
			robot.controller.BottomRightOff()
		if mag == 3:
			robot.controller.TopRightOn()
		else:
			robot.controller.TopRightOff()

	def Heading(self):
		# Read the Euler angles for heading, roll, pitch (all in degrees).
		while True:
			try:   #PUTTING HEADING IN TRY EXCEPT

				heading = 0
				heading, roll, pitch = self.bno.read_euler()
				#sys, gyro, accel, mag = bno.get_calibration_status()


			except RuntimeError:
				print("coudn't read of compass tryed again")
				continue

			else:
				break


		return heading
	def Calibrated(self):
		sys, gyro, accel, mag = self.bno.get_calibration_status()
		return True if min([sys,gyro,accel,mag]) == 3 else False
	def CalibValues(self):
		sys, gyro, accel, mag = self.bno.get_calibration_status()
		return (sys,gyro,accel,mag)

	def Values(self):
		return self.bno.get_calibration()
	def SetValues(self,values):
		for i in range(10):
			try:
				self.bno.set_calibration(values)
			except:
				if i == 4:
					raise RuntimeError("Compass still can't be written to")



rTotal = 0
bTotal = 0
gTotal = 0
class Camera:
	def __init__(self):
		import picamera
		self.started = False
	def start(self,res=(64,64),frate=10): #res 32,32 and frate 80
		if not self.started:
			self.cam=picamera.PiCamera()
			self.resolution=res
			#self.cam.resolution=res
			#self.cam.framerate=frate
			time.sleep(2)
			self.started = True
			self.cam.contrast = (-5)
			self.cam.brightness = (55)
			self.cam.zoom = (0.2,0.4,0.6,1)
			#self.cam.contrast(50)

	def DanielPhoto2(self, numPhotos=5):
		rTotal = 0
		gTotal = 0
		bTotal = 0
		count = 0
		stream = io.BytesIO()
		for foo in self.cam.capture_continuous(stream, format='jpeg' , resize=self.resolution, use_video_port=True):
			# Truncate the stream to the current position (in case
			# prior iterations output a longer image)
			stream.truncate()
			stream.seek(0)
			img = Image.open(stream)
			img.save("{}.jpeg".format(1))
			pixels = list(img.getdata())
			#pixels = pixels[5*32:-16*32]
			for pixle in pixels:
				rTotal+=pixle[0]
				gTotal+=pixle[1]
				bTotal+=pixle[2]
			count += 1
			if count >= numPhotos:
				return (rTotal/numPhotos,gTotal/numPhotos,bTotal/numPhotos)



	def DanielPhoto(self, numPhotos):
		self.cam.resolution=self.resolution
		global rTotal
		global bTotal
		global gTotal
		rTotal = 0
		bTotal = 0
		gTotal = 0
		def outputs(numPhotos):
			global rTotal
			global bTotal
			global gTotal
			stream = io.BytesIO()
			for i in range(numPhotos):
				yield stream
				stream.seek(0)
				img = Image.open(stream)
				for pixle in list(img.getdata()):
					rTotal+=pixle[0]
					gTotal+=pixle[1]
					bTotal+=pixle[2]
				stream.seek(0)
				stream.truncate()

		self.cam.capture_sequence(outputs(numPhotos), 'jpeg', use_video_port=True)
		rTotal = rTotal/numPhotos
		gTotal = gTotal/numPhotos
		bTotal = bTotal/numPhotos
		return (rTotal,gTotal,bTotal)




class Ultra:
	def __init__(self,echo,trigger):
		self.echo = echo
		self.trigger = trigger
		GPIO.setup(self.echo,GPIO.IN)
		GPIO.setup(self.trigger, GPIO.OUT)

	def reset(self):
		GPIO.output(self.trigger, GPIO.LOW)


	def distance(self,reset=True):
		if reset:
			self.reset()
			time.sleep(0.01)#0.001 worked
		GPIO.output(self.trigger, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(self.trigger, GPIO.LOW)
		failSafe=time.time()
		while True:
			pulse_start_time = time.time()
			if GPIO.input(self.echo)!=0 or time.time()-failSafe>0.001:
				break
		while True: #Remove this
			pulse_end_time = time.time()
			if not (GPIO.input(self.echo)==1 and time.time()-pulse_start_time < 0.01):
				break
		pulse_duration = pulse_end_time - pulse_start_time
		distance = round(pulse_duration * 17150, 2)
		if int(distance) == 0:
			return self.distance()
		return int(distance)

class Robot:
	def __init__(self):
		self.NebSpeed = 1
		self.ultraBackRightSide = Ultra(18,27)
		self.ultraBackRight = Ultra(4,17)
		self.ultraFrontRight = Ultra(22,23)
		self.ultraFrontRightSide = Ultra(25,5)

		self.ultraBackLeftSide = Ultra(26,21)
		self.ultraBackLeft = Ultra(20,19)
		self.ultraFrontLeft = Ultra(6,16)
		self.ultraFrontLeftSide = Ultra(13,12)
		self.ZB = ThunderBorg3.ThunderBorg()
		self.ZB.Init()
		self.reverse=0
		print(self.ZB.GetBatteryReading())
		self.leftSpeed = 0
		self.rightSpeed = 0
		print("waiting for remote")
		while True:
			try:
				self.controller=xbox.Joystick()
				break
				#self.controller.startstart()
			except:
				time.sleep(0.5)
				# remove this just to not have to have remote
		self.camera=Camera()
		print("waiting for compass")
		self.compass=Compass()
		self.compass.Start() #remove if no compass
		print("blasting sensors")
		for i in range(1000):
			print(i)
			self.simRead([self.ultraFrontRight,self.ultraFrontLeft,self.ultraBackRight,self.ultraBackLeft,self.ultraFrontRightSide,self.ultraFrontLeftSide,self.ultraBackRightSide,self.ultraBackLeftSide,])
			self.compass.Heading()

	def simRead(self,ultras):
		distances=[]
		for ultra in ultras:
			ultra.reset()
		time.sleep(0.01)
		for ultra in ultras:
			distances.append(ultra.distance(reset=False))
		return distances

	def stayDeg(self,stopCond,deg,absolute=False,maxSpeed=1,params=[]):
		if absolute:
			targetHeading=deg%360
		else:
			targetHeading=(self.compass.Heading()+deg)%360
		def tempStopCond():
			return abs(self.WhichWay(self.compass.Heading(),targetHeading))<15 #
		if stopCond=="turned":
			stopCond=tempStopCond
		while not stopCond(*params) or not tempStopCond():
			currentHeading=self.compass.Heading()
			print(currentHeading)
			offset=self.WhichWay(currentHeading,targetHeading)
			if offset>2:
				self.forward(maxSpeed,maxSpeed*self.AmountToReduce(abs(offset)))
			elif offset<-2:
				self.forward(maxSpeed*self.AmountToReduce(abs(offset)),maxSpeed)
			else:
				self.forward(maxSpeed,maxSpeed)

	def stayMid(self,stopCond,dist,rightSide=False,maxSpeed=1,params=[]):
		while not stopCond(*params):
			ChangeInSpeed = 0.5
			if not rightSide:
				F = self.ultraFrontLeftSide.distance()
				B = self.ultraBackLeftSide.distance()
			else:
				B = self.ultraFrontRightSide.distance()
				F = self.ultraBackRightSide.distance()
			if F < 150 and B < 150:
				change = 0.35*(F-B) + 0.23*((F+B)/2-dist)
				ChangeInSpeed+=change
			lspeed,rspeed=maxSpeed*0.5/max(abs(0.5),abs(ChangeInSpeed)),maxSpeed*ChangeInSpeed/max(abs(0.5),abs(ChangeInSpeed))
			#print([F,B,lspeed,rspeed])
			#rspeed,lspeed=0.5/max(0.5,ChangeInSpeed),ChangeInSpeed/max(0.5,ChangeInSpeed)
			#print(lspeed,rspeed)
			self.forward(lspeed,rspeed)
			#if self.ultraFrontLeftSide.distance() > 40:
			#	robot.stop()
			#	break
	def stayMid2(self,stopCond,dist,rightSide=True,maxSpeed=1,params=[],targetHeading="current",simRead=True):
		global last
		last=robot.ultraFrontRight.distance()
		if targetHeading=="current":
			targetHeading=(self.compass.Heading())%360
		def close(dist=55):
			global last
			distRead = robot.ultraFrontRight.distance()
			if abs(last-distRead)<20:
				print("test",distRead)
				last=distRead
				return distRead<dist # FIX when breadboard is finnished
			else:
				last=distRead
				return close(dist)
		leftSide=1^rightSide
		while not stopCond(*params): # may require to be set to while true for maze
			last=robot.ultraFrontRight.distance()
			currentHeading=self.compass.Heading()
			offset=self.WhichWay(currentHeading,targetHeading)
			if leftSide:
				if simRead:
					F,B,front1,front2 = self.simRead([self.ultraFrontLeftSide,self.ultraBackLeftSide,self.ultraFrontRight,self.ultraFrontLeft])
					#if abs((front1/front2)-1)<0.1:
					#	if front1+front2<110:
					#		break
					print(front1)
					if close(front1):
						print("stayMidTurn")
						break
				else:
					F,B = self.simRead([self.ultraFrontLeftSide,self.ultraBackLeftSide])
				avDist=(F+B)/2
				offset2=dist-avDist
			else:
				if simRead:
					F,B,front = self.simRead([self.ultraFrontRightSide,self.ultraBackRightSide,self.ultraFrontRight])
					if front<55:
						break
				else:
					F,B = self.simRead([self.ultraFrontRightSide,self.ultraBackRightSide])
				avDist=(F+B)/2
				offset2=avDist-dist
			#print(offset,offset2)
			#time.sleep(0.1)
			offset+=min(offset2,offset,key=abs)
			if offset>2:
				self.forward(maxSpeed,maxSpeed*self.AmountToReduce(abs(offset)))
			elif offset<-2:
				self.forward(maxSpeed*self.AmountToReduce(abs(offset)),maxSpeed)
			else:
				self.forward(maxSpeed,maxSpeed)
	def GoingStraight(self,SPEED,Constant,Constant2,Constant3):
		while not self.controller.Y():
			self.forward(0,0)
			manual.rc()
			if self.controller.A():
				heading = self.compass.Heading()
				self.forward(SPEED,SPEED)
				while self.controller.A():
					direction = self.WhichWay(heading,self.compass.Heading())
					if direction > 0:
						if direction > Constant3:
							self.forward(SPEED * Constant, SPEED)
						else:
							self.forward(SPEED * Constant2, SPEED)
					else:
						if direction < -Constant3:
							self.forward(SPEED, SPEED * Constant)
						else:
							self.forward(SPEED, SPEED * Constant2)


	def MazeMid(self,SPEED):
		while True:
			ChangeInSpeed = 0
			FL = robot.ultraFrontLeft.distance()  #NEED TO BE UPDATED FOR CORRECT ULTRASONIC SENSOR
			BL = robot.ultraBackLeft.distance()
			if FL < 40 and BL < 40:
				ChangeInSpeed = (FL-BL)*0.13 - (10-(FL+BL)/2)/20
			if ChangeInSpeed > 1:
				ChangeInSpeed = 1
			if ChangeInSpeed < -1:
				ChangeInSpeed = -1
			robot.forward(SPEED-ChangeInSpeed,SPEED+ChangeInSpeed)


	def setController(self,controller):
		self.controller=controller
		self.camera.cam.close()

	def shutdown(self):
		try:
			GPIO.cleanup()
		except:
			pass
		try:
			self.controller.close()
		except:
			pass
		try:
			self.camera.cam.close()
		except:
			pass
		try:
			self.stop()
		except:
			pass
		print("Processes Safely Stopped")

	def Voltage(self):
		print(self.ZB.GetBatteryReading())

	def arcneg90(self,speed,degBefore):
		robot.forward(speed,speed)
		time.sleep(0.5)
		initialHeading = robot.compass.Heading()
		FinalHeading = (initialHeading - 90)%360
		robot.forward(0,speed)

		while self.WhichWay(robot.compass.Heading(),FinalHeading) < -degBefore:
			pass
		robot.forward(speed,speed)
		time.sleep(0.5)
		robot.stop()

	def PerfectArcRight(self,L,R):
		robot.forward(L,R)
		while robot.ultraFrontLeft.distance() > 20:
			pass
		robot.stop()

	def turn(self,power):
		self.forward(power,-power)

	def forward(self,speed1,speed2):
		if not self.reverse:
			self.ZB.SetMotor1(speed1)
			self.ZB.SetMotor2(-speed2) #Remove /2
			self.rightSpeed = speed2
			self.leftSpeed = speed1
		else:
			self.ZB.SetMotor1(-speed2)
			self.ZB.SetMotor2(speed1) #Remove /2
			self.rightSpeed = speed1
			self.leftSpeed = speed2


	def SoftStop(self,timeTo = 0.5):
		DecL = (self.leftSpeed/100) * -1
		DecR = (self.rightSpeed/100) * -1
		for i in range(100):
			self.inc(DecL, DecR)
			time.sleep(timeTo/100)
	#good for nebula robot.mstop5(38,-0.4,10,1)  robot.stop5(38,-0.3,12,1)
	def BackAndReverse(self,speed,disToStop,Heading):
		robot.forward(-speed,-speed)
		while robot.ultraFrontLeft.distance() < disToStop:
			pass
		robot.TurnDegreesOp2(2,Heading)

	def stop5Forwards(self,DisStartSlowing,BackSpeed,StopDis,Forwards,HeadingNeeded=False):
		BeenTrued = False
		print("using Stop5")
		readings = []
		speeds = []
		HeadingNeeded = HeadingNeeded % 360
		count = 0
		if Forwards:
			prevSpeed = 1
			StartSpeed = self.NebSpeed
			robot.forward(StartSpeed,StartSpeed)

			whichUltra = [robot.ultraFrontRight,robot.ultraFrontLeft]
			BackSpeed = abs(BackSpeed)*-1
		else:
			prevSpeed = -self.NebSpeed
			StartSpeed = -1
			robot.forward(StartSpeed,StartSpeed)

			whichUltra = [robot.ultraBackLeft,robot.ultraBackRight]
			BackSpeed = abs(BackSpeed)
		counting = 0
		count = 0
		prev = 0
		while prev < 20:
			prev = min([whichUltra[0].distance(),whichUltra[1].distance()])
		while True:
			count += 1
			counting += 1
			disleft = min([whichUltra[0].distance(),whichUltra[1].distance()])
			print(disleft)
			if abs(prev-disleft) > 20:
				continue
			prev = disleft
			if disleft < DisStartSlowing and count > 3:
				if disleft < 13 and disleft > 3 or robot.controller.X():#StopDis or robot.controller.X(): testing bigger stop dis
					#robot.stop()
					break

				Speed = ((disleft-StopDis)/(DisStartSlowing-StopDis))*(StartSpeed-BackSpeed) + BackSpeed
				if prevSpeed * Speed < 0: # removed equal sign for testing NEEDS FURTHER TESTING
					count += 1
				prevSpeed = Speed # check this because I think it prevents it reversing
				if count == 2:
					print("using this part annoyingly")
					if StartSpeed > 0:
						robot.forward(0.3,0.3)
					else:
						robot.forward(-0.3,-0.3)
					while min([whichUltra[0].distance(),whichUltra[1].distance()]) > 10 or robot.controller.X():
						pass
					#robot.stop()
					break
				if Speed < 0.3 and Speed >=0:
					Speed = 0.3
					robot.forward(0.3,0.3)
				elif Speed > -0.3 and Speed < 0:
					Speed = -0.3
					robot.forward(-0.3,-0.3)
				else:

					robot.forward(Speed,Speed)
			else:
				if HeadingNeeded:
					Speed = StartSpeed
					direction = self.WhichWay(HeadingNeeded,self.compass.Heading())
					if abs(direction) > 100 and not BeenTrued:
						HeadingNeeded = (HeadingNeeded-180) % 360
						direction = self.WhichWay(HeadingNeeded,self.compass.Heading())
						BeenTrued = True
					if direction > 2:
						if StartSpeed > 0:
							robot.forward(StartSpeed*self.AmountToReduce(abs(direction)),StartSpeed)
						else:
							robot.forward(StartSpeed,StartSpeed*self.AmountToReduce(abs(direction)))
					elif direction < -2:
						if StartSpeed > 0:
							robot.forward(StartSpeed,StartSpeed*self.AmountToReduce(abs(direction)))
						else:
							robot.forward(StartSpeed*self.AmountToReduce(abs(direction)),StartSpeed)
					else:
						robot.forward(StartSpeed,StartSpeed)
			readings.append(disleft)
			speeds.append(Speed)
		print("while loop ran {} times".format(counting))
		return readings,speeds


	#Not Bad robot.back5(22,0.1,55,-1)
	def back5(self,DisStartSlowing,BackSpeed,StopDis,Backwards,HeadingNeeded=False):
		BeenTrued = False
		print("Using Back5")
		HeadingNeeded = HeadingNeeded % 360
		if Backwards:
			StartSpeed = -0.6#self.NebSpeed
			robot.forward(StartSpeed,StartSpeed)
			whichUltra = [robot.ultraFrontRight,robot.ultraFrontLeft]
			BackSpeed = abs(BackSpeed)
		else:
			StartSpeed = 0.6#self.NebSpeed
			robot.forward(StartSpeed,StartSpeed)
			whichUltra = [robot.ultraBackLeft,robot.ultraBackLeft]
			BackSpeed = -abs(BackSpeed)

		while True:
			disleft = min([whichUltra[0].distance(),whichUltra[1].distance()])
			print(disleft)
			if disleft > DisStartSlowing:
				if disleft > StopDis:
					robot.stop()
					break
				Speed = ((disleft-StopDis)/(DisStartSlowing-StopDis))*(StartSpeed-BackSpeed) + BackSpeed
				if Speed < 0.3 and Speed >= 0:
					robot.forward(0.3,0.3)
				elif Speed > -0.3 and Speed < 0:
					robot.forward(-0.3,-0.3)
				else:
					robot.forward(Speed,Speed)
			if HeadingNeeded:

				direction = self.WhichWay(HeadingNeeded,self.compass.Heading())
				if abs(direction) > 100 and not BeenTrued:
					HeadingNeeded = (HeadingNeeded-180) % 360

					direction = self.WhichWay(HeadingNeeded,self.compass.Heading())
					BeenTrued = True
				if direction > 2:
					if StartSpeed > 0:
						robot.forward(StartSpeed*self.AmountToReduce(abs(direction)),StartSpeed)
					else:
						robot.forward(StartSpeed,StartSpeed*self.AmountToReduce(abs(direction)))
				elif direction < -2:
					if StartSpeed > 0:
						robot.forward(StartSpeed,StartSpeed*self.AmountToReduce(abs(direction)))
					else:
						robot.forward(StartSpeed*self.AmountToReduce(abs(direction)),StartSpeed)
				else:
					robot.forward(StartSpeed,StartSpeed)


	def stop(self):
		self.forward(0,0)

	def inc(self,IncL,IncR):
		#if self.rightSpeed + IncR > 1 or self.rightSpeed + IncR < -1 or self.leftSpeed + IncL > 1 or self.leftSpeed < -1:
		#	raise Exception("Cant increment motors above 1 or below -1")
		self.rightSpeed += IncR
		self.leftSpeed += IncL
		self.forward(self.leftSpeed,self.rightSpeed)

	def WhichWay(self,Now,WhereGo):
		return((WhereGo-Now+180)%360-180)


	def TurnDegreesOp1(self,Degrees,absHeading=False):
			Start = robot.compass.Heading()
			if absHeading:
				EndDeg = absHeading%360
			else:
				EndDeg = (Start + Degrees) % 360

			if self.WhichWay(Start,EndDeg) > 0:
				robot.turn(1)
			else:
				robot.turn(-1)
			while True:
				if abs(self.WhichWay(robot.compass.Heading(),EndDeg)) < 2:
					robot.stop()
					break

	def bestTimeCalib(self,degrees):
		startDegrees = degrees - 40
		prevaccuracy = 10000000
		for degreeTest in range(startDegrees,degrees,2):
			origHeading = self.compass.Heading()
			self.TurnDegreesOp1(degreeTest)
			finalHeading = self.compass.Heading()
			accuracy = abs(self.WhichWay((origHeading+degrees)%360,finalHeading))
			print(accuracy)
			if accuracy > prevaccuracy:
				print(degreeTest)
				robot.stop()
				break
			prevaccuracy = accuracy
			time.sleep(1)

	def degreesandTry(self,degreesaiming,degreesTry):
		startHead = self.compass.Heading()
		robot.TurnDegreesOp1(degreesTry)
		time.sleep(1)
		FinalHead = self.compass.Heading()
		print("off by:")
		print(self.WhichWay((startHead+degreesaiming)%360,FinalHead))

	def degreesandTryTime(self,timeToTry,DegreesWanted):
		startHead = self.compass.Heading()
		robot.turn(1)
		time.sleep(timeToTry)
		robot.stop()
		time.sleep(1)
		FinalHead = self.compass.Heading()
		print("off By")
		print(self.WhichWay((startHead+DegreesWanted)%360,FinalHead))
	def TurnDegreesOp2(self,Degrees,absHeading=-873.56):
			Start = robot.compass.Heading()
			if absHeading != -873.56:
				EndDeg = absHeading%360
			else:
				EndDeg = (Start + Degrees) % 360

			PosOrNeg = self.WhichWay(Start,EndDeg)
			print(PosOrNeg)
			if self.WhichWay(Start,EndDeg) > 0:

				robot.turn(1)
			else:

				robot.turn(-1)
			disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
			while disleft * PosOrNeg > 0 and abs(disleft) > 30:
				disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
				 # need better way to check signs opposite

			robot.stop()
			time.sleep(0.1)
			PosOrNeg = self.WhichWay(robot.compass.Heading(),EndDeg)
			if PosOrNeg > 0:
				power = 1
			else:
				power = -1
			while self.WhichWay(robot.compass.Heading(),EndDeg) * PosOrNeg > 0:
				self.jigTurn(power = power)
				time.sleep(0.05)

	def ForBack(self):
		heading = robot.compass.Heading()
		robot.stop5Forwards(33,-0.8,10,True,heading)
		robot.back5(32,-0.3,40,True,heading)
		robot.stop()

	def RepeatTurn(self,absHeading):
		BiggestAllowableAngleOff = 20 # changed from 20
		Start = robot.compass.Heading()
		print(Start)
		print(absHeading)
		EndDeg = absHeading%360
		PosOrNeg = self.WhichWay(Start,EndDeg)
		if self.WhichWay(Start,EndDeg) > 0:

			robot.turn(1)
		else:

			robot.turn(-1)
		disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
		whatToTurn = 10 #changed from 30
		while disleft * PosOrNeg > 0 and abs(disleft) > whatToTurn:
			disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
			 # need better way to check signs opposite
		robot.stop()
	def TurnDegreesOp3(self,Degrees,absHeading=-873.56):
			BiggestAllowableAngleOff = 5
			Start = robot.compass.Heading()
			print(Start)
			if absHeading != -873.56:
				EndDeg = absHeading%360
			else:
				EndDeg = (Start + Degrees) % 360
				absHeading = EndDeg

			PosOrNeg = self.WhichWay(Start,EndDeg)
			if self.WhichWay(Start,EndDeg) > 0:

				robot.turn(1)
			else:

				robot.turn(-1)
			disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
			if disleft > 50:
				whatToTurn = 27
			else:
				whatToTurn = 15
			while disleft * PosOrNeg > 0 and abs(disleft) > whatToTurn:
				disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
				#print(robot.compass.Heading())
				 # need better way to check signs opposite

			robot.stop()
			time.sleep(0.1)

			disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
			if abs(disleft) < BiggestAllowableAngleOff:
				return None
			#time.sleep(1)
			self.RepeatTurn(absHeading)

	def AmountToReduce(self,absDirection):
		speedMin = 0
		AngleMax = 10
		if absDirection > AngleMax:
			return speedMin
		return 1.4-((((absDirection-2)/(AngleMax-2))*(1-speedMin)) + speedMin)

	def TurnDegreesOp3WithJigging(self,Degrees,absHeading=-873.56):
			print("Turning")
			Start = robot.compass.Heading()
			if absHeading != -873.56:
				EndDeg = absHeading%360
			else:
				EndDeg = (Start + Degrees) % 360

			PosOrNeg = self.WhichWay(Start,EndDeg)
			if self.WhichWay(Start,EndDeg) > 0:

				robot.turn(1)
			else:

				robot.turn(-1)
			disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
			if disleft > 50:
				whatToTurn = 27
			else:
				whatToTurn = 15
			while disleft * PosOrNeg > 0 and abs(disleft) > whatToTurn:
				disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
				 # need better way to check signs opposite

			robot.stop()
			time.sleep(0.1)
			disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
			while abs(disleft) > 2: #trying much bigger error test probably need to put 5 back to 1
				if disleft > 0:
					self.jigTurn(power = 1)
				else:

					self.jigTurn(power = -1)
				disleft = self.WhichWay(robot.compass.Heading(),EndDeg)
				time.sleep(0.05)

	def mazeSection(self,useless1, useless2, maxSpeed = 1,targetHeading = "random",rightSide=True,DisToStop = 50,DisToBe=22,threshold=4):
		if targetHeading == "random":
			targetHeading == self.compass.Heading()
		Heading = targetHeading
		Speed = maxSpeed
		def DisToWall(rightSide):
			if rightSide:
				F,B,InFront1,InFront2 = self.simRead([self.ultraFrontRightSide, self.ultraBackRightSide,self.ultraFrontRight, self.ultraFrontLeft])
				return (F+B)/2,(InFront1+InFront2)/2
			F,B,InFront1,InFront2 = self.simRead([self.ultraFrontLeftSide,self.ultraBackLeftSide,self.ultraFrontRight, self.ultraFrontLeft])
			return (F+B)/2,(InFront1+InFront2)/2
		anglesRead = []
		UltraAverages = []
		FrontUltras = []
		HeadingNeededs = []
		prevReading = -100000
		while True:
			DisToWallNow,InFront = DisToWall(rightSide)
			UltraAverages.append(DisToWallNow)
			FrontUltras.append(InFront)
			print(DisToWallNow, InFront)
			if prevReading - InFront > 20:
				pass
			else:
				print("here")
				if InFront < 50:
					break
				prevReading = InFront
			angle = ((DisToWallNow-5)/(39-5))*(20--20) + - 20
			HeadingNeeded = (Heading + angle)%360
			HeadingNeededs.append(HeadingNeeded)
			direction = self.WhichWay(HeadingNeeded,self.compass.Heading())
			anglesRead.append(direction)
			#print(direction)
			if direction >2:
				if Speed > 0:
					self.forward(Speed*self.AmountToReduce(abs(direction)),Speed)
				else:
					self.forward(Speed,Speed*self.AmountToReduce(abs(direction)))
			elif direction <-2:
				if Speed > 0:
					self.forward(Speed,Speed*self.AmountToReduce(abs(direction)))
				else:
					self.forward(Speed*self.AmountToReduce(abs(direction)),Speed)
			else:
				self.forward(Speed,Speed)
		with open('staymidnums.pkl', 'wb') as f:
			pickle.dump([anglesRead,UltraAverages,FrontUltras,HeadingNeededs], f)
		robot.stop()
	def jigTurn(self,power=1,timet=0.02): # put to 0.02 with full speed
		self.turn(power)
		time.sleep(timet)
		self.stop()
	def getSpeed(self):
		return (self.leftSpeed,self.rightSpeed)

	def softEval(self, val1,val2):
	    return val1/val2<1.4 and val1/val2>0.7

	def classify(self, r,g,b):
	    m=r
	    r,g,b=r/m,g/m,b/m
	    if g>r and not softEval(g,r):
	        return "green"

	    elif r>g and not softEval(r,g) and r>b and not softEval(r,b):
	        return "red"
	    elif b>r and not softEval(b,r) and b>g and not softEval(b,g):
	        return "blue"
	    elif r>b and not softEval(r,b) and g>b and not softEval(g,b):
	        return "yellow"
	    else:
	        return "black"
robot=Robot()
atexit.register(robot.shutdown) #GREAT LINE
'''import io
import time
import picamera
with picamera.PiCamera() as camera:
stream = io.BytesIO()
for foo in camera.capture_continuous(stream, format='jpeg'):
# Truncate the stream to the current position (in case
# prior iterations output a longer image)
stream.truncate()
stream.seek(0)
if process(stream):
break '''
import manual
