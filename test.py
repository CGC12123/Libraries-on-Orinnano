'''
带通信

'''

import cv2
import cv2 as cv
import numpy as np
# from communite_module.Communications import SelfSerial
from loguru import logger
import math
import time



def find_biggest(image, color):
    target_corlor = color
    flag = 0 # 标志位，识别到为1

    target_x = 0
    target_y = 0
    temp_distance = 0

    low = color_dist[target_corlor]['lower'] # 阈值设置
    high = color_dist[target_corlor]['high']

    image_gaussian = cv.GaussianBlur(image, (5, 5), 0)     # 高斯滤波
    imgHSV = cv.cvtColor(image_gaussian, cv.COLOR_BGR2HSV) # 转换色彩空间

    kernel = np.ones((5,5),np.uint8)  # 卷积核
    mask = cv.erode(imgHSV, kernel, iterations=2)
    mask = cv.dilate(mask, kernel, iterations=1)
    mask = cv.inRange(mask, low, high)
    cnts = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2] # 检测外轮廓
    try:
        for i in cnts:
            perimeter = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.02*perimeter,True) # 角的数量
            rect = cv2.minAreaRect(i)
            box = cv2.boxPoints(rect)
            cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
            left_point_x = np.min(box[:, 0])
            right_point_x = np.max(box[:, 0])
            top_point_y = np.min(box[:, 1])
            bottom_point_y = np.max(box[:, 1])
            
            mid_point_x = (left_point_x + right_point_x)/2 # 理应除以2，但为了传输数据不超过256选择舍弃个位
            mid_point_y = (top_point_y + bottom_point_y)/2
            
            mid_point_x = round(mid_point_x, 2) # 保留两位小数
            mid_point_y = round(mid_point_y, 2)

            distance = (((mid_point_x - 320) ** 2) + ((mid_point_y - 240) ** 2))**0.5

            if((distance < temp_distance) or temp_distance == 0):
                target_x = mid_point_x
                target_y = mid_point_y
                temp_distance = distance
        #print("coordinate is (%d, %d)" %(target_x, target_y))
        flag = 1
        
    except :
        #print("get failed")
        target_x = 0
        target_y = 0
        temp_distance = 0
        
    #image = cv.flip(image, 1) # 镜像操作
    cv.imshow('camera', image)
    cv.waitKey(1)
    msg = (flag, ) + get_gigh_low_data(int(target_x)) + get_gigh_low_data(int(target_y))
    return msg # 返回坐标

# 数据处理函数
def get_gigh_low_data(data):
    temp_h = data >> 8
    temp_l = data - (temp_h << 8)
    return (temp_h, temp_l)


if __name__ == "__main__":
    #  定义颜色字典
    color_dist = {  'blue': {'lower':np.array([98, 112, 75]), 'high':np.array([179, 255, 255])},
                    'red': {'lower':np.array([0, 196, 104]), 'high':np.array([179,255,255])},
                    }

    # self_serial = SelfSerial("/dev/ttyAMA1")
    # cap = cv.VideoCapture(2)# 下摄像头
    cap = cv.VideoCapture(0)# 前摄像头
    model = 0 # 模式
    target_shape = ' '
    target_color = ' '
    while True:
        # model = self_serial.uart_read_mode(model)
        #识别匹配目标颜色与形状
        model = 10
        if model == 0: # 发送上线消息
            # self_serial.uart_send_msg(0, (1, ))
            pass

        elif model == 10 : # 任务一返回距离最近的物体坐标

            ret, frame = cap.read()
            if ret:
                msg = find_biggest(frame, 'red')
            
                logger.info(msg)
                if msg:
                    # self_serial.uart_send_msg(20, msg)
                    print(msg)


        elif model == 50:
            pass