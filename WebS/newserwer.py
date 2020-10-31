import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import sensor4
from tornado.options import define, options, parse_command_line
import RPi.GPIO as GPIO
import time
import motorLib as motors
import autonomic
import keepgoing


connection = []
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)

class SensorsObject:
    front = 0
    left  = 0
    right = 0
    rear  = 0
    def __repr__(self):
        return "FD: %s LD: %s RD: %s BD: %s" % (self.front, self.left, self.right, self.rear)
    def __str__(self):
        return "FD:%s LD:%s RD:%s BD:%s" % (self.front, self.left, self.right, self.rear)
    def assign(self,data):
        self.front = data.front
        self.left = data.left
        self.right = data.right
        self.rear = data.rear

class MotorPower:
    def __init__(self,left,right,time = 2):
        self.left = left
        self.right = right
        self.time = time
    left  = 0
    right = 0
    time  = 2

global sensorsData
global motorData
global AUTO_MODE_1
global AUTO_MODE_2

def light_led_on_connect():
    GPIO.output(12,GPIO.HIGH)

def light_led_off_disconnect():
    GPIO.output(12,GPIO.LOW)

def send_sensor_data():
    global connection
    global sensorsData
    global AUTO_MODE_1
    global AUTO_MODE_2
    while True:
        time.sleep(0.6)
        for c in connection:
            try:
                sensorsData.assign(sensor4.dist())
                print sensorsData
                if AUTO_MODE_1:
                    print "SERVER: Check collision"
                    autonomic.checkCollision(sensorsData)
                if AUTO_MODE_2:
                    print "SERVER: Check collision"
                    keepgoing.checkCollision(sensorsData)
                c.write_message(str(sensorsData))
            except:
                print("Distance send error")
                motors.stop()

define("port", default=8888, type=int)

def do_action(msg):
    global motorData
    global AUTO_MODE_1
    global AUTO_MODE_2
    if msg == "FRONT":
        motors.forward(motorData)
    elif msg == "STOP":
        motors.stop()
    elif msg == "LEFT":
        motors.left(motorData)
    elif msg == "RIGHT":
        motors.right(motorData)
    elif msg == "BACK":
        motors.back(motorData)
    elif msg == "TLEFT":
        motors.turnleft(motorData)
    elif msg == "TRIGHT":
        motors.turnright(motorData)
    elif msg == "A1GO":
        AUTO_MODE_1 = True
        autonomic.start(motorData)
    elif msg == "A2GO":
        AUTO_MODE_2 = True
        autonomic.start(motorData)
    elif msg == "ASTOP":
        AUTO_MODE_1 = False
        AUTO_MODE_2 = False
        motors.stop()
    else:
        msg = msg.split()
        if len(msg) == 3:
            leftpower = msg[0].split(":")
            rightpower = msg[1].split(":")
            turntime = msg[2].split(":") 
            if leftpower[0] == "LP":
                motorData.left = 40*int(leftpower[1])
            if rightpower[0] == "RP":
                motorData.right = 40*int(rightpower[1])
            if turntime[0] == "TT":
                motorData.time = float(turntime[1])/1000.0
 
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        global connection
        print("New Connection")
        light_led_on_connect()
        self.write_message("update")
        connection = [self]

    def on_message(self, message):
        do_action(str(message))

    def on_close(self):
        print("Connection closed")
        light_led_off_disconnect()


app = tornado.web.Application([
    (r'/ws/', WebSocketHandler),
])


if __name__ == '__main__':
    global sensorsData
    global motorData
    global AUTO_MODE_1
    global AUTO_MODE_2
    AUTO_MODE_1 = False
    AUTO_MODE_2 = False
    motorData = MotorPower(2000,2000,2)
    sensorsData = SensorsObject()
    threadSensor = threading.Thread(target = send_sensor_data)
    threadSensor.start()
    connection = []
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
