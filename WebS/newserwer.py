import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import sensor4
from tornado.options import define, options, parse_command_line
import RPi.GPIO as GPIO
import time
import stop
import forward
import left
import right
import back
import autonomic
import turnleft
import turnright

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
global AUTO_MODE

def light_led_on_connect():
    GPIO.output(12,GPIO.HIGH)

def light_led_off_disconnect():
    GPIO.output(12,GPIO.LOW)

def send_sensor_data():
    global connection
    global sensorsData
    global AUTO_MODE
    while True:
        time.sleep(0.6)
        for c in connection:
            try:
                sensorsData.assign(sensor4.dist())
                print sensorsData
                if AUTO_MODE:
                    print "SERVER: Check collision"
                    autonomic.checkCollision(sensorsData)
                c.write_message(str(sensorsData))
            except:
                print("Distance send error")
                stop.now()

define("port", default=8888, type=int)

def do_action(msg):
    global motorData
    global AUTO_MODE
    if msg == "FRONT":
        forward.now(motorData)
    elif msg == "STOP":
        stop.now()
    elif msg == "LEFT":
        left.now(motorData)
    elif msg == "RIGHT":
        right.now(motorData)
    elif msg == "BACK":
        back.now(motorData)
    elif msg == "TLEFT":
        turnleft.now(motorData)
    elif msg == "TRIGHT":
        turnright.now(motorData)
    elif msg == "AGO":
        AUTO_MODE = True
        autonomic.start(motorData)
    elif msg == "ASTOP":
        AUTO_MODE = False
        stop.now()
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
        connection = []
        connection.append(self)

    def on_message(self, message):
        do_action(str(message))

    def on_close(self):
        print("Connection closed")
        light_led_off_disconnect()


app = tornado.web.Application([
    (r'/ws/', WebSocketHandler),
])


if __name__ == '__main__':
    global leftPOWER
    global rightPOWER
    global sensorsData
    global motorData
    global AUTO_MODE
    AUTO_MODE = False
    motorData = MotorPower(2000,2000,2)
    sensorsData = SensorsObject()
    threadSensor = threading.Thread(target = send_sensor_data)
    threadSensor.start()
    connection = []
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
