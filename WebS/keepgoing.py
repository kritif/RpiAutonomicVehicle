import motorLib as motors
import time

global motorData
global orientation

class MotorData:
    def __init__(self,left,right,time):
        self.left  = left
        self.right = right
        self.time_left  = time
        self.time_right = time
        self.left_p_left = left
        self.right_p_left = right
        self.left_p_right = left
        self.right_p_right = right

    def assign(self,data):
        self.left  = data.left
        self.right = data.right
        self.time_left = data.time_left
        self.time_right = data.time_right
        self.left_p_left = data.left_p_left
        self.right_p_left = data.right_p_left
        self.left_p_right = data.left_p_right
        self.right_p_right = data.right_p_right

    left  = 1800
    right = 1800
    time_left  = 2
    time_right = 2
    left_p_left = 0
    right_p_left = 0
    left_p_right = 0
    right_p_right = 0

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
        if int(data.front) <= 20:
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
            time.sleep(0.5)
            motors.stop()
            motors.turnright(motorData)
            orientation = "forward"
            motors.forward(motorData)
    elif orientation == "right":
        if int(data.left) > 40:
            time.sleep(0.5)
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
