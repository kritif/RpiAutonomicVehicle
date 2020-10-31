import motorLib as motors
import time

global motorData
global orientation

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
    global orientation
    print "AUTONOMIC MODE: Started"
    global motorData
    motorData = MotorData(0,0,0)
    motorData.assign(data)
    motors.forward(motorData)
    orientation = 'forward'

def checkCollision(data):
    global motorData
    global orientation
    print "AUTONOMIC MODE: Check Collision"
    if orientation == 'forward':
        if int(data.front) <= 15:
            motors.stop()
            orientation = makeDecision(data)
            if orientation == "left":
                print "AUTONOMIC MODE: Turn left"
                motors.forward(motorData)
            if orientation == "right":
                print "AUTONOMIC MODE: Turn right"
                motors.forward(motorData)
    elif orientation == "left":
        if int(data.right) > 40:
            motors.stop()
            motors.turnright(motorData)
            orientation = "forward"
            motors.forward(motorData)
    elif orientation == "right":
        if int(data.left) > 40:
            motors.stop()
            motors.turnleft(motorData)
            orientation = "forward"
            motors.forward(motorData)
    elif orientation == "error":
        print "AUTOOMIC MODE: error"

def makeDecision(data):
    global motorData
    global orientation
    if orientation == "forward":
        if int(data.left) > int(data.right):
            motors.turnleft(motorData)
            return "left"
        if int(data.left) <= int(data.right):
            motors.turnright(motorData)
            return "right"
    elif orientation == "left":
        return
    elif orientation == "right":
        return
    return "error"
