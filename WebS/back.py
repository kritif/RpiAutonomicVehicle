import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685(address=0x60,busnum=1)
pwm.set_pwm_freq(1000)
def now(data):
    pwm.set_pwm(2,0,data.left)
    pwm.set_pwm(3,0,0)
    pwm.set_pwm(4,4096,0)
    pwm.set_pwm(7,0,data.right)
    pwm.set_pwm(6,0,0)
    pwm.set_pwm(5,4096,0)
