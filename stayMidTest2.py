from robotFunctions import *
def false():
    return False
def stayMid2(stopCond,dist,leftSide=True,maxSpeed=1,params=[]):
    targetHeading=(robot.compass.Heading())%360
    time.sleep(1)
    targetHeading=(robot.compass.Heading())%360
    print("read heading")
    for i in range(10):
        print(10-i)
        time.sleep(1)
    def tempStopCond():
        return abs(robot.WhichWay(robot.compass.Heading(),targetHeading))<10
    if stopCond=="turned":
        stopCond=tempStopCond
    while not stopCond(*params) or not tempStopCond():
        currentHeading=robot.compass.Heading()
        offset=robot.WhichWay(currentHeading,targetHeading)
        if leftSide:
            F,B = robot.simRead([robot.ultraFrontLeftSide,robot.ultraBackLeftSide])
            avDist=(F+B)/2
            offset2=dist-avDist
        else:
            F,B = robot.simRead([robot.ultraFrontRightSide,robot.ultraBackRightSide])
            avDist=(F+B)/2
            offset2=avDist-dist
        #print(offset,offset2)
        #time.sleep(0.1)
        offset+=min(offset2,offset,key=abs)
        if offset>2:
            robot.forward(maxSpeed,maxSpeed*robot.AmountToReduce(abs(offset)))
        elif offset<-2:
            robot.forward(maxSpeed*robot.AmountToReduce(abs(offset)),maxSpeed)
        else:
            robot.forward(maxSpeed,maxSpeed)
stayMid2(false,22,leftSide=False)
