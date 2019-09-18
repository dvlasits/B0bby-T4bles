#!/usr/bin/env python3
#quit()
import sys
import os
from robotFunctions import *
import time
import warnings
import maze
import speedTest
import nebula
#import rgb
count = 1
robot.compass.Start()
robot.camera.start()
maxSpeed=1
try:
    while True:
        count -= 1
        if count == 0:
            print("attempting initiation")
            count = 100000
        if robot.controller.A():
            if robot.controller.dpadDown():
                reverse=robot.reverse
                robot.reverse=0
                maze.run()
                robot.reverse=reverse
            elif robot.controller.dpadLeft():
                robot.reverse=0
                nebula.run()
            elif robot.controller.dpadRight():
                robot.reverse=0
                speedTest.run()
            elif robot.controller.dpadUp():
                #rgb.toggle()
                #gun stuff
                pass

        if robot.controller.connected():
            if robot.controller.dpadUp():
                maxSpeed=min(1,maxSpeed+0.1)
                time.sleep(0.2)
            elif robot.controller.dpadDown():
                maxSpeed=max(0.5,maxSpeed-0.1)
                time.sleep(0.2)
            if robot.controller.Y():
                robot.reverse=robot.reverse^1
                time.sleep(0.2)

            if robot.controller.rightTrigger():
                if robot.controller.leftX() < -0.2:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.rightTrigger()*abs(1-abs(robot.controller.leftX()))),(max(maxSpeed,0.8)*robot.controller.rightTrigger()))
                elif robot.controller.leftX() > 0.2:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.rightTrigger()),(max(maxSpeed,0.8)*robot.controller.rightTrigger()*abs(1-abs(robot.controller.leftX()))))
                else:
                    robot.forward((maxSpeed*robot.controller.rightTrigger()),(maxSpeed*robot.controller.rightTrigger()))

            elif robot.controller.leftTrigger():
                if robot.controller.leftX() > 0.2:
                    robot.forward((max(maxSpeed,0.8)*-robot.controller.leftTrigger()*abs(1-abs(robot.controller.leftX()))),(max(maxSpeed,0.8)*-robot.controller.leftTrigger()))
                elif robot.controller.leftX() < -0.2:
                    robot.forward((max(maxSpeed,0.8)*-robot.controller.leftTrigger()),(max(maxSpeed,0.8)*-robot.controller.leftTrigger()*abs(1-abs(robot.controller.leftX()))))
                else:
                    robot.forward((maxSpeed*-robot.controller.leftTrigger()),(maxSpeed*-robot.controller.leftTrigger()))
            elif robot.controller.leftBumper():
                robot.turn((-0.9))
            elif robot.controller.rightBumper():
                robot.turn((0.9))
            else:
                if abs(robot.controller.leftY()-robot.controller.rightY())<0.5:
                    robot.forward((maxSpeed*robot.controller.leftY()),(maxSpeed*robot.controller.rightY()))
                else:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.leftY()),(max(maxSpeed,0.8)*robot.controller.rightY()))
        else:
            robot.stop()


        if robot.controller.Back():
            robot.shutdown()
            quit("Stopped interface.py")
except Exception as e:
    with open("crash.log","w+") as f:
        f.write(str(e))
