import sys
from loguru import logger
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')

import Jetson.GPIO as GPIO
import time

def GpioInit(output_pin, value: bool = 0, clean: bool = 0):
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW) # 设置引脚 初始为低
    if value:
        curr_value = GPIO.HIGH
    else:
        curr_value = GPIO.LOW
    
    logger.info("Outputting {} to pin {}".format(curr_value, output_pin))
    GPIO.output(output_pin, curr_value)
    curr_value ^= GPIO.HIGH

    if clean:
        GPIO.cleanup()

'''
T: 20ms
0.5ms
STOP: 1.5ms
>1.5ms fan

2.5max
'''


def GpioPwm(output_pin):
    '''
    
    '''
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
    p = GPIO.PWM(output_pin, 50)
    # p.start(0)
    # p.ChangeDutyCycle(10)
    p.stop()

    # time.sleep(0.1)


if __name__ == '__main__':
    GpioInit(7, value=1)
    time.sleep(1)
    GpioInit(7, value=0)
    time.sleep(1)
    # GpioInit(7, value=1)
    # time.sleep(1)
    # GpioInit(7, value=0)
    # time.sleep()