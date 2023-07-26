import sys
from loguru import logger
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')

import Jetson.GPIO as GPIO
import time


def main():
    # 设置GPIO模式为BCM模式
    GPIO.setmode(GPIO.BCM)

    # 定义PWM信号的GPIO引脚
    pwm_pin = 7

    # 设置GPIO引脚为输出模式
    GPIO.setup(pwm_pin, GPIO.OUT)

    # 定义PWM信号的周期和占空比
    period = 0.2  # 20ms
    duty_cycle = 1  # 50%的占空比

    # 计算PWM信号的高电平时间和低电平时间
    high_time = period * duty_cycle
    low_time = period - high_time

    # 循环输出PWM信号
    while True:
        # 输出高电平
        GPIO.output(pwm_pin, GPIO.HIGH)
        time.sleep(high_time)
        
        # 输出低电平
        GPIO.output(pwm_pin, GPIO.LOW)
        time.sleep(low_time)

if __name__ == '__main__':
    main()
