import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685(address=0x60,busnum=1)
pwm.set_pwm_freq(1000)


def forward(data):
    pwm.set_pwm(2, 0, data.left)
    pwm.set_pwm(3, 4096, 0)
    pwm.set_pwm(4, 0, 0)
    pwm.set_pwm(7, 0, data.right)
    pwm.set_pwm(6, 4096, 0)
    pwm.set_pwm(5, 0, 0)


def right(data):
    pwm.set_pwm(2, 0, data.left)
    pwm.set_pwm(3, 4096, 0)
    pwm.set_pwm(4, 0, 0)
    pwm.set_pwm(7, 0, data.right)
    pwm.set_pwm(6, 0, 0)
    pwm.set_pwm(5, 4096, 0)


def left(data):
    pwm.set_pwm(2, 0, data.left)
    pwm.set_pwm(3, 0, 0)
    pwm.set_pwm(4, 4096, 0)
    pwm.set_pwm(7, 0, data.right)
    pwm.set_pwm(6, 4096, 0)
    pwm.set_pwm(5, 0, 0)


def back(data):
    pwm.set_pwm(2, 0, data.left)
    pwm.set_pwm(3, 0, 0)
    pwm.set_pwm(4, 4096, 0)
    pwm.set_pwm(7, 0, data.right)
    pwm.set_pwm(6, 0, 0)
    pwm.set_pwm(5, 4096, 0)


def stop():
    pwm.set_pwm(2, 0, 0)
    pwm.set_pwm(3, 4096, 0)
    pwm.set_pwm(4, 0, 0)
    pwm.set_pwm(7, 0, 0)
    pwm.set_pwm(6, 4096, 0)
    pwm.set_pwm(5, 0, 0)


def turnleft(data):
    left(data)
    time.sleep(data.time)
    stop()


def turnright(data):
    right(data)
    time.sleep(data.time)
    stop()
