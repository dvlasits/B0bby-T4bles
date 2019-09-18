import RPi.GPIO as GPIO
import time
import random
GPIO.setmode(GPIO.BCM)
def toggle():
    rgb.toggle()
class RGB:
    def __init__(self,rStart,gStart,bStart):
        pinR=None # Add the red pin here
        pinG=None # Add the green pin here
        pinB=None # Add the blue pin here

        self.modes={0:self.constant,1:self.random}
        GPIO.setup(pinR,GPIO.OUT)#pin for Red
        GPIO.setup(pinG,GPIO.OUT)#pin for Green
        GPIO.setup(pinB,GPIO.OUT)#pin for blue
        self.r=GPIO.PWM(pinR,frequency)
        self.g=GPIO.PWM(pinG,frequency)
        self.b=GPIO.PWM(pinB,frequency)
        self.rVal=rStart
        self.gVal=gStart
        self.bVal=bStart
        self.r.start(rVal)
        self.g.start(gVal)
        self.b.start(bVal)
        self.enabled=False
        self.toggle() # remove if we want the robot to start with lights on
        self.mode=self.modes[0]
    def toggle():
        self.enabled=self.enabled^1
        if self.enabled:
            mode()
        else:
            self.r.ChangeDutyCycle(0)
            self.g.ChangeDutyCycle(0)
            self.b.ChangeDutyCycle(0)
    def constant():
        self.r.ChangeDutyCycle(self.rVal)
        self.g.ChangeDutyCycle(self.gVal)
        self.b.ChangeDutyCycle(self.bVal)
    def rainbow():
        self.r.ChangeDutyCycle(random.random())
        self.g.ChangeDutyCycle(random.random())
        self.b.ChangeDutyCycle(random.random())

rgb=RGB(1,1,1)
