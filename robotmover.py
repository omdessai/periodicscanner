import RPi.GPIO as GPIO
import google.oauth2.credentials
import time
import commands

class Mover:
    def __init__(self, scancb):
        self.scancallback = scancb
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(19, GPIO.IN)

    def __del__(self):
        GPIO.cleanup()
    
    def checkdist():
        GPIO.output(26, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(26, GPIO.LOW)
        while not GPIO.input(19):
            pass
        t1 = time.time()
        while GPIO.input(19):
            pass
        t2 = time.time()
        return (t2-t1)*340/2

    def setunsetpin(self, pin, delay):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pin, GPIO.LOW)
    
    def setunsettwopins(self, pin1, pin2, delay):
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)

    def move(self, direction, steps):
        print("moving direction ->", direction, " steps -> ", steps)
        if(direction == commands.Direction.BACKWARD):
            for i in range(0, steps):
                self.setunsetpin(23, .5)
        if(direction == commands.Direction.FORWARD):
            for i in range(0, steps):
                self.setunsetpin(18, .5)
        if(direction == commands.Direction.LEFTBACKWARD):
            for i in range(0, steps):
                self.setunsettwopins(23, 25, .5)
        if(direction == commands.Direction.LEFTFORWARD):
            for i in range(0, steps):
                self.setunsettwopins(18, 25, .5)
        if(direction == commands.Direction.RIGHTBACKWARD):
            for i in range(0, steps):
                self.setunsettwopins(23, 12, .5)
        if(direction == commands.Direction.RIGHTFORWARD):
            for i in range(0, steps):
                self.setunsettwopins(18, 12, .5)
        
        self.scancallback()
        #print("Moving "+ direction.name() + " by " + steps + " steps")
        #print("Moving")

    def adjust(self):
        print("Adjusting to scan element")
        self.setunsetpin(18, .1)
