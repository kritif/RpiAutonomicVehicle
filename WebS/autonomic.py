import motorLib as motors
import time

global motorData

class MotorData:
    def __init__(self,left,right,time):
        self.left  = left
        self.right = right
        self.time  = time

    def assign(self,data):
        self.left  = data.left
        self.right = data.right
        self.time  = data.time

    left  = 1800
    right = 1800
    time  = 2

def start(data):
    print "AUTONOMIC MODE: Started"
    global motorData
    motorData = MotorData(0,0,0)
    motorData.assign(data)
    motors.forward(motorData)

def checkCollision(data):
    global motorData
    print "AUTONOMIC MODE: Check Collision"
    if int(data.front) <= 15:
        #stop.now()
        motors.stop()
        direction = makeDecision(data)
        if direction == "left":
            print "AUTONOMIC MODE: Turn left"
            motors.forward(motorData)
        if direction == "right":
            print "AUTONOMIC MODE: Turn right"
            motors.forward(motorData)
        if direction == "error":
            print "AUTOOMIC MODE: error"

def makeDecision(data):
    global motorData
    if int(data.left) > int(data.right):
        motors.turnleft(motorData)
        return "left"
    if int(data.left) <= int(data.right):
        motors.turnright(motorData)
        return "right"
    return "error"
