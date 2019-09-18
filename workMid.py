from robotFunctions import *
def stayMid(stopCond,dist,rightSide=False,maxSpeed=1,params=[]):
                while not stopCond(*params):
                        ChangeInSpeed = 0.5
                        if not rightSide:
                                F,B=robot.simRead([robot.ultraFrontLeftSide,robot.ultraBackLeftSide])
                        else:
                                F,B = robot.simRead([robot.ultraFrontRightSide,robot.ultraBackRightSide])
                        if F < 150 and B < 150:
                                change = 0.04*(F-B) + (0.03*((F+B)/2-dist))*abs(0.05*((F+B)/2-dist))
                                if not rightSide:
                                        ChangeInSpeed+=change
                                        if change>0:
                                                rspeed = 1
                                                lspeed = 6#tochange
                                        ChangeInSpeed-=change
                                time.sleep(0.2)
                                print(change)
                        #robot.forward(lspeed,rspeed)

def Trueing():
	return False

stayMid(Trueing,30,rightSide=True,maxSpeed = 1)
manual.rc()
