
#33,-0.3,12

Stop5ForwardsParamsTrue = [33,-0.8,10,True]
Stop5ForwardsParamsFalse = [33,-0.8,10,False]
Back5ParamsFalse = [22,-0.3,30,False]
Back5ParamsTrue = [22,-0.3,30,True]
'''Stop5ForwardsParamsTrue = [33,-0.4,9,True] for 0.8 I think
Stop5ForwardsParamsFalse = [33,-0.4,9,False]
Back5ParamsFalse = [20,-0.3,35,False]
Back5ParamsTrue = [20,-0.3,35,True]'''
Stop5ForwardsParamsTrue = [40,-0.1,10,True] # 26 was 30
Stop5ForwardsParamsFalse = [40,-0.1,10,False]
'''Back5ParamsFalse = [32,-0.3,40,False]
Back5ParamsTrue = [32,-0.3,40,True]for faster speeds ish of 1 unreliable though'''
'''Back5ParamsFalse = [29,-0.3,37,False]
Back5ParamsTrue = [29,-0.3,37,True] for speed of 0.8 back this is verry good'''
Back5ParamsFalse = [32,0,35,False]
Back5ParamsTrue = [32,0,35,True]
from robotFunctions import *
def listofWhat(RedNum,BlueNum,YellowNum,GreenNum,IsAngle = False,absHeading=0):
    global Stop5ForwardsParamsTrue
    global Stop5ForwardsParamsFalse
    global Back5ParamsFalse
    global Back5ParamsTrue
    RedNumHeading = (absHeading + 45 + (RedNum-1)*90)%360
    BlueNumHeading = (absHeading + 45 + (BlueNum - 1)*90)%360
    GreenNumHeading = (absHeading + 45 + (GreenNum-1)*90)%360
    YellowNumHeading = (absHeading + 45 + (YellowNum - 1)*90)%360
    global roboHeading
    roboHeading = 0
    global operations
    operations = []
    global parameters
    parameters = []
    global roboDirection
    roboDirection = 0
    whatToTurn = robot.WhichWay(absHeading,RedNumHeading)
    if IsAngle:
        roboHeading = 315
        whatToTurn = robot.WhichWay(roboHeading,RedNumHeading)
        if whatToTurn == 0:
            operations.append(robot.stop5Forwards)
            a = list(Stop5ForwardsParamsTrue)
            a.append(roboHeading)
            parameters.append(a)
            roboDirection = 1
        elif abs(whatToTurn) == 180:
            #roboHeading = (roboHeading + whatToTurn) % 360
            operations.append(robot.stop5Forwards)
            a = list(Stop5ForwardsParamsFalse)
            a.append(roboHeading)
            parameters.append(a)
            roboDirection = -1
        else:
            roboHeading = (roboHeading + whatToTurn) % 360
            operations.append(roboHeading)
            operations.append(robot.stop5Forwards)
            a = list(Stop5ForwardsParamsTrue)
            a.append(roboHeading)
            parameters.append(a)
            roboDirection = 1


    else:
        if  whatToTurn == 45 or round(whatToTurn) == -45:
            roboDirection = 1

            roboHeading = (roboHeading + whatToTurn) % 360
            operations.append(roboHeading)
            operations.append(robot.stop5Forwards)
            a = list(Stop5ForwardsParamsTrue)
            a.append(roboHeading)
            parameters.append(a)
            roboDirection = 1
        else:
            if whatToTurn < 0:

                roboHeading = (roboHeading + 45) % 360
                operations.append(roboHeading)
                a = list(Stop5ForwardsParamsFalse)
                a.append(roboHeading)
                operations.append(robot.stop5Forwards)
                parameters.append(a)
                roboDirection = -1
            else:
                roboHeading = (roboHeading - 45) % 360
                operations.append(roboHeading)
                a = list(Stop5ForwardsParamsFalse)
                a.append(roboHeading)
                operations.append(robot.stop5Forwards)
                parameters.append(a)
                roboDirection = -1
    def doing(NextHeading):
        global operations
        global roboHeading
        global roboDirection
        whatToTurn = robot.WhichWay(roboHeading,NextHeading)
        if whatToTurn == 0:
            #operations.append(roboHeading)
            a = list(Stop5ForwardsParamsTrue)
            a.append(roboHeading)
            operations.append(robot.stop5Forwards)
            parameters.append(a)

            roboDirection = roboDirection*-1
        elif whatToTurn == 180 or whatToTurn == -180:
            #operations.append(roboHeading)
            a = list(Stop5ForwardsParamsFalse)
            a.append(roboHeading)
            operations.append(robot.stop5Forwards)
            parameters.append(a)

            roboDirection = roboDirection*-1
        else:
            if roboDirection == 1:
                a = list(Back5ParamsTrue)
                a.append(roboHeading)
                operations.append(robot.back5)
                parameters.append(a)
            else:
                a = list(Back5ParamsFalse)
                a.append(roboHeading)
                operations.append(robot.back5)
                parameters.append(a)
            roboHeading = (roboHeading + whatToTurn) % 360
            a = list(Stop5ForwardsParamsTrue)
            a.append(roboHeading)
            operations.append(roboHeading)
            operations.append(robot.stop5Forwards)
            parameters.append(a)
            roboDirection = 1
    doing(BlueNumHeading)
    doing(YellowNumHeading)
    doing(GreenNumHeading)
    return operations,parameters
print(listofWhat(1,2,3,4,IsAngle = True))
