import cv2
import numpy as np
import os

from communite_module.Communications import SelfSerial
from tools.SplitInt import get_high_low_data
from loguru  import logger

os.system('echo 123456 | sudo -S chmod 777 /dev/ttyUSB1')

ball_color = 'red'

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }

cap = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)

self_serial = SelfSerial('/dev/ttyUSB1')

mode = 0

check = 1 # 防止二次进入键盘输入

logger.info("System Starting")

while True:
    ret, frame = cap.read()
    

    if ret:
        
        mode = self_serial.uart_read_mode(mode)
        # mode = 2

        # if mode == 0:
        #     self_serial.uart_send_msg(0x01, msg)
        # if mode == 99:
        #     pass
        if mode == 2:
            if frame is not None:
                gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
                hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
                erode_hsv = cv2.erode(hsv, None, iterations=2)
                inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
                cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                try:
                    c = max(cnts, key=cv2.contourArea)
                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                    cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
                    x = ([np.int0(box)][0][0][0] + [np.int0(box)][0][2][0]) / 2
                    y = ([np.int0(box)][0][0][1] + [np.int0(box)][0][2][1]) / 2
                    x = int(x)
                    y = int(y)
                    print(x, y)
                except:
                    x = 0
                    y = 0
                                                                                                                                                                                                                                   
                # logger.info('{},{}', format(x, y))
                msg = get_high_low_data(x) + get_high_low_data(y)
                self_serial.uart_send_msg(0x02, msg)
        if mode == 1:
            if frame is not None:
                print("请输入")
                x1 = int(input())
                y1 = int(input())
                x2 = int(input())
                y2 = int(input())
                # x3 = int(input())
                # y3 = int(input())

                # print(x1,y1)
                # print(x2,y2)
                # x1 = 100
                # y1 = 100
                # x2 = 150
                # y2 = 100
                msg = get_high_low_data(x1) + get_high_low_data(y1) + get_high_low_data(x2) + get_high_low_data(y2)
                self_serial.uart_send_msg(0x01, msg) 
                mode = 99
        if mode == 3:
            pass

        if mode == 99:
            pass
        # cv2.imshow('camera', frame)
        # cv2.waitKey(1)
