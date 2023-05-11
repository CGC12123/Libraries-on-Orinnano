import cv2
from loguru import logger
import numpy as np
from pyzbar import pyzbar
import pytesseract
import os

class Detections():
    def __init__(self, image):
        # 颜色字典
        self.color_dist = { 'blue': {'lower':np.array([98, 112, 75]), 'high':np.array([179, 255, 255])},
                            'red': {'lower':np.array([0, 113, 174]), 'high':np.array([13,255,255])}}
        # 画面
        self.image = image
        # 检测到目标的标志位
        self.flag = 0
        # 检测目标的中心点坐标
        self.target_x = 0 
        self.target_y = 0
        # 距离目标距离
        self.distance = 0
        # 识别到的二维码信息
        self.qrcode_message = 0
        # 字符识别识别到的字符
        self.character_message: str = '0'

        self.img_num = len(os.listdir('./vis/det_color'))

    # 找寻最大色块
    def find_biggest_color(self, color, show: bool = 1):
        low = self.color_dist[color]['lower'] # 阈值设置
        high = self.color_dist[color]['high']

        image_gaussian = cv2.GaussianBlur(self.image, (5, 5), 0)     # 高斯滤波
        imgHSV = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV) # 转换色彩空间

        kernel = np.ones((5,5),np.uint8)  # 卷积核
        mask = cv2.erode(imgHSV, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.inRange(mask, low, high)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] # 检测外轮廓
        try:
            max_contour = max(cnts, key=cv2.contourArea)
            rect = cv2.minAreaRect(max_contour)
            box = cv2.boxPoints(rect)
            cv2.drawContours(self.image, [np.int0(box)], -1, (0, 255, 255), 2)
            left_point_x = np.min(box[:, 0])
            right_point_x = np.max(box[:, 0])
            top_point_y = np.min(box[:, 1])
            bottom_point_y = np.max(box[:, 1])
            
            mid_point_x = (left_point_x + right_point_x)/2
            mid_point_y = (top_point_y + bottom_point_y)/2
            
            mid_point_x = round(mid_point_x, 2) # 保留两位小数
            mid_point_y = round(mid_point_y, 2)

            # distance = (((mid_point_x - 320) ** 2) + ((mid_point_y - 240) ** 2))**0.5 # 去年的代码 现在不知道干什么用的了

            self.target_x = mid_point_x
            self.target_y = mid_point_y
            #print("coordinate is (%f, %f)" %(target_x, target_y))
            self.flag = 1
            
        except :
            #print("get failed")
            self.target_x = 0
            self.target_y = 0
            self.flag = 0
            pass

        logger.info('{}, {}'.format(int(self.target_x), int(self.target_y)))

        if show:
            # image = cv2.flip(image, 1) # 镜像操作 使用笔记本摄像头可用
            cv2.imshow('red', self.image)
            cv2.waitKey(1)

    # 寻找二维码或条形码
    def detect_qrcode(self, show: bool = 1):
        barcodes = pyzbar.decode(self.image) # 检测码
        for barcode in barcodes: # 循环读取检测到的码
            # 绘条形码、二维码多边形轮廓
            points =[]
            for point in barcode.polygon:
                points.append([point[0], point[1]])
            points = np.array(points,dtype=np.int32).reshape(-1,1, 2)
            cv2.polylines(self.image, [points], True, color=(0,0,255),thickness=2)

            # 条形码数据为字节对象，将其转换成字符串
            barcodeData = barcode.data.decode("UTF-8") #先解码成字符串
            barcodeType = barcode.type
            # 绘出图像上的条形码数据和类型
            self.qrcode_message = "({}): {} ".format(barcodeType, barcodeData)
            logger.info(self.qrcode_message)
        
        if show:
            # img = cv2.flip(img, 1) # 镜像操作
            cv2.imshow("QR", self.image)
            cv2.waitKey(1) 

    # 字符识别
    def detect_character(self, mode: str = '', show: bool = 1):

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        boxes = pytesseract.image_to_boxes(img_gray)

        for box in boxes.splitlines():
            # print(box)
            box = box.split(' ')
            if box[0] == 'A':
                x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
                cv2.rectangle(img, (x, 640 - y), (w, 480 - h), (0, 0, 255), 2)

                mid_x = (x + w)/2
                mid_y = (640 + 480)/2

                print("(%d, %d)" %(mid_x,mid_y))
            
        # cv.rectangle(img_edge, top_left, bottom_right, (0,255,0), 2) # 测试用，在轮廓图上画框

        img = cv2.flip(img, 1) # 镜像操作
        cv2.imshow('camera', img)
        cv2.waitKey(1)