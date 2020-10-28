import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

FRONT_TRIGGER = 21
FRONT_ECHO    = 23
LEFT_TRIGGER  = 20
LEFT_ECHO     = 27
RIGHT_TRIGGER = 4
RIGHT_ECHO    = 18
BACK_TRIGGER  = 19
BACK_ECHO     = 17

class SensorDistance:
    front = 0
    left  = 0
    right = 0
    rear  = 0

#F_DIST = 0
#L_DIST = 0
#R_DIST = 0
#b_DIST = 0

GPIO.setmode(GPIO.BCM)

def dist():
    sensorsDist = SensorDistance()
    GPIO.setup(FRONT_TRIGGER,GPIO.OUT)
    GPIO.setup(LEFT_TRIGGER,GPIO.OUT)
    GPIO.setup(RIGHT_TRIGGER,GPIO.OUT)
    GPIO.setup(BACK_TRIGGER,GPIO.OUT)
    GPIO.setup(FRONT_ECHO,GPIO.IN)
    GPIO.setup(LEFT_ECHO,GPIO.IN)
    GPIO.setup(RIGHT_ECHO,GPIO.IN)
    GPIO.setup(BACK_ECHO,GPIO.IN)
    GPIO.output(FRONT_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(FRONT_TRIGGER,False)

    while GPIO.input(FRONT_ECHO) == 0:
        FStartTime = time.time()
    while GPIO.input(FRONT_ECHO) == 1:
        FStopTime = time.time()

    GPIO.output(LEFT_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(LEFT_TRIGGER,False)

    while GPIO.input(LEFT_ECHO) == 0:
        LStartTime = time.time()
    while GPIO.input(LEFT_ECHO) == 1:
        LStopTime = time.time()

    GPIO.output(RIGHT_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(RIGHT_TRIGGER,False)

    while GPIO.input(RIGHT_ECHO) == 0:
        RStartTime = time.time()
    while GPIO.input(RIGHT_ECHO) == 1:
        RStopTime = time.time()

    GPIO.output(BACK_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(BACK_TRIGGER,False)

    while GPIO.input(BACK_ECHO) == 0:
        BStartTime = time.time()
    while GPIO.input(BACK_ECHO) == 1:
        BStopTime = time.time()
    
    sensorsDist.front = distance(FStartTime,FStopTime)
    sensorsDist.left  = distance(LStartTime,LStopTime)
    sensorsDist.right = distance(RStartTime,RStopTime)
    sensorsDist.rear  = distance(BStartTime,BStopTime)
    return sensorsDist
#return "FD:"+str(F_DIST)+" LD:"+str(L_DIST)+" RD:"+str(R_DIST)+" BD:"+str(B_DIST)

def distance(stime,etime):
    return int(((etime - stime) * 34300) / 2)

if __name__ == "__main__":
    print (dist())
