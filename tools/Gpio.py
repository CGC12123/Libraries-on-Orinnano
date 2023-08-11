import sys
import time
from loguru import logger
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')

import Jetson.GPIO as GPIO

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

def GpioPwm(output_pin):
    # 未完成测试
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
    p = GPIO.PWM(output_pin, 50)
    # p.start(0)
    # p.ChangeDutyCycle(10)
    # p.stop()

    # time.sleep(0.1)


if __name__ == '__main__':
    pass