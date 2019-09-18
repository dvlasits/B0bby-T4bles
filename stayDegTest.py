from robotFunctions import *
heading = robot.compass.Heading()
print(heading)
heading-=90
heading=-90
print(heading)
def false():
    return robot.ultraFrontRight.distance()<55
robot.stayDeg(false,heading,absolute=False,maxSpeed=1,params=[])
heading=90
robot.stayDeg(false,heading,absolute=False,maxSpeed=1)
robot.stayDeg(false,heading,absolute=False,maxSpeed=1)
heading=-90
robot.stayDeg(false,heading,absolute=False,maxSpeed=1)
robot.stayDeg(false,heading,absolute=False,maxSpeed=1)
