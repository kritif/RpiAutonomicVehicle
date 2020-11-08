import motorLib as motors
import time

global motorData

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

def start(data,track):
    print "AUTONOMIC MODE: Started"
    global motorData
    track = track.split(";")
    motorData = MotorData(0,0,0)
    motorData.assign(data)
    for task in track:
        taskData = task.split(":")
        if taskData[0] == "front":
            motors.forward(motorData)
            time.sleep(float(taskData[1]))
            motors.stop()
        if taskData[0] == "left":
            motors.left(motorData)
            time.sleep(float(taskData[1]))
            motors.stop()
        if taskData[0] == "right":
            motors.right(motorData)
            time.sleep(float(taskData[1]))
            motors.stop()
        if taskData[0] == "back":
            motors.back(motorData)
            time.sleep(float(taskData[1]))
            motors.stop()




