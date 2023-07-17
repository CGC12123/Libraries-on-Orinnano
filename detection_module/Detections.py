import cv2
from loguru import logger
import numpy as np
from pyzbar import pyzbar
import pytesseract
import torch
import sys 
import json

class Detections():
    def __init__(self, image):
        # 颜色字典
        self.color_dist = { 'blue': {'lower':np.array([98, 112, 75]), 'high':np.array([179, 255, 255])},
                            'red': {'lower':np.array([115, 101, 0]), 'high':np.array([179,255,255])},
                            'black': {'lower':np.array([0, 0, 0]), 'high':np.array([180,255,50])}}
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
        self.character_message: str = ' '
        # 形状识别识别到的形状
        self.shape = ' '

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
            self.flag = 1
            
        except :
            self.target_x = 0
            self.target_y = 0
            self.flag = 0
            pass

        logger.info('{}, {}'.format(int(self.target_x), int(self.target_y)))

        if show:
            # image = cv2.flip(image, 1) # 镜像操作 使用笔记本摄像头可用
            cv2.imshow('find_biggest_color', self.image)
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
            cv2.imshow("detect_qrcode", self.image)
            cv2.waitKey(1) 

    # 字符识别
    def detect_character(self, mode: str = 'get position', character: str = '', show: bool = 1):
        '''
        mode:
            get position: 找特殊字符的位置
                character: 待识别的字符
                    此算法使用流畅性很低
            get character: 识别字符 (待更新)
        '''
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        boxes = pytesseract.image_to_boxes(img_gray)
        if mode == 'get position':
            for box in boxes.splitlines():
                box = box.split(' ')
                if box[0] == character:
                    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
                    cv2.rectangle(self.image, (x, 640 - y), (w, 480 - h), (0, 0, 255), 2)

                    self.target_x = (x + w)/2
                    self.target_y = (640 + 480)/2

                    logger.info('character positon: ', self.target_x, self.target_y)
            
        # cv.rectangle(img_edge, top_left, bottom_right, (0,255,0), 2) # 测试用，在轮廓图上画框

        # self.image = cv2.flip(self.image, 1) # 镜像操作
        if show: 
            cv2.imshow('detect_character', self.image)
            cv2.waitKey(1)

    # 工具函数
    def angle_cos(self, p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2) ) )

    # 识别形状
    def detect_shape(self, mode: str = None, specify_color: str = None, target_shape = ' ', show: bool = 1):
        '''
        mode:
            get shape: 寻找最大的那个形状
            get location: 找距离中心最近的
        
        special_color:
            指定要识别的物体的颜色

        taeget_shape:
            在模式get location中所需要检测的物体形状
                Triangle / Square / Circle
        '''
        image_gaussian = cv2.GaussianBlur(self.image, (5, 5), 0)     # 高斯滤波
        imgHSV = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV) # 转换色彩空间

        kernel = np.ones((5,5),np.uint8)  # 卷积核
        mask = cv2.erode(imgHSV, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=1)
        if specify_color is not None:
            low = self.color_dist[specify_color]['lower']
            high = self.color_dist[specify_color]['high']
            mask = cv2.inRange(mask, low, high) # 筛选对应颜色
        
        imgcanny = cv2.Canny(mask, 0, 100) # 颜色范围内边缘检测
        if mode == 'get shape':
            try:
                cnts = cv2.findContours(imgcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] # 检测外轮廓
                area_max = max(cnts, key = cv2.contourArea) # 得到最大轮廓
                rect = cv2.minAreaRect(area_max)     # 绘制每个轮廓的最小外接矩形的方法
                box = cv2.boxPoints(rect)            # 获取矩形的四个顶点坐标
                cv2.drawContours(self.image, [np.int0(box)], -1, (0, 255, 255), 2)    # 绘制矩形

                area = cv2.contourArea(area_max)
                perimeter = cv2.arcLength(area_max,True)
                approx = cv2.approxPolyDP(area_max,0.02*perimeter,True)
                CornerNum = len(approx) # 角的数量
                rect = cv2.minAreaRect(area_max)
                box = cv2.boxPoints(rect)
                x, y, w, h = cv2.boundingRect(approx)
                if CornerNum ==3:
                    self.shape = 'Triangle'
                    logger.info('{}'.format(self.shape))
                elif 4>=CornerNum and CornerNum <= 7:
                    self.shape = 'Square'
                    logger.info('{}'.format(self.shape))
                elif CornerNum>7:
                    self.shape = 'Circle'
                    logger.info('{}'.format(self.shape))
                else:
                    self.shape = 'NULL'
            except:
                self.shape = 'NULL'
        elif mode == 'get location':
            r_cnts = []
            target_recognize = ' '
            cnts = cv2.findContours(imgcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] # 检测外轮廓
            for c in cnts:
            # rect = cv2.minAreaRect(c)     # 绘制每个轮廓的最小外接矩形的方法
            # box = cv2.boxPoints(rect)            # 获取矩形的四个顶点坐标
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.045 * peri, True)

                CornerNum = len(approx)     # 角的数量
                if CornerNum == 3:
                    target_recognize = 'Triangle'
                elif  CornerNum == 4:
                    if len(approx) == 4 and cv2.isContourConvex(approx):
                        target_recognize = 'Null'
                        approx = approx.reshape(-1, 2)
                        max_cos = np.max([self.angle_cos(approx[i], approx[(i+1) % 4], approx[(i+2) % 4]) for i in range(4)])
                        # 只检测矩形（cos90° = 0）
                        if 0 <= max_cos <= 0.3:
                            target_recognize = 'Square'
                        else:
                            break
                elif CornerNum > 4:
                    target_recognize = 'Circle'
                else:
                    target_recognize = 'NULL'

                if target_recognize == target_shape:   # 在天上识别到的和目标相同时返回目标坐标
                    cv2.drawContours(self.image, [c], -1, (0, 255, 0), 2)
                    M = cv2.moments(c)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])
                        r_cnts.append((x, y))

            if len(r_cnts) == 1:
                self.target_x = int(x)
                self.target_y = int(y)

            elif len(r_cnts) == 2:
                x1 = r_cnts[0][0]
                y1 = r_cnts[0][1]
                x2 = r_cnts[1][0]
                y2 = r_cnts[1][1]
                
                # 根据所求更改要的坐标
                if ((x1 - 230) ** 2 + (y1 - 240) ** 2) ** 0.5 > ((x2 - 230) ** 2 + (y2 - 240) ** 2) ** 0.5:
                    self.target_x = x2
                    self.target_y = y2
                else:
                    self.target_x = x1
                    self.target_y = y1

            logger.info('{}, {}'.format(int(self.target_x), int(self.target_y)))

        if show:
            cv2.imshow('detect_shape', self.image)
            cv2.waitKey(1)

    # YOLOV5识别
    def detect_obj_yolov5(self, detect_target: str = None, model = None, show = 0):
        if model is not None:
            image = self.image
            results = model(image)
            # 将结果转为json数据
            json_data = results.pandas().xyxy[0].to_json(orient="records")
            # 解析 JSON 数据
            try:
                data = json.loads(json_data)
                for d in data:
                    # 匹配目标
                    if d['name'] == detect_target:
                        self.target_x = int((d['xmin'] + d['xmax']) / 2)
                        self.target_y = int((d['ymin'] + d['ymax']) / 2)
                        image = results.render()[0]
                    else:
                        self.target_x = 0
                        self.target_y = 0
            except:
                self.target_x = 0
                self.target_y = 0
            logger.info('{}, {}'.format(int(self.target_x), int(self.target_y)))

        if show:
            cv2.imshow("detect_obj_yolov5", image)
            cv2.waitKey(1)

    def detect_obj_yolov8(self, detect_target: str = None, model = None, show = 0):
        if model is not None:
            image = self.image
            results = model(image)
            try:
                boxes = results[0].boxes
                tensor = (boxes[0].xyxy)[0]
                values = tensor.cpu().numpy()
                self.target_x = int((values[0] + values[2]) / 2)
                self.target_y = int((values[1] + values[3]) / 2)
            except:
                self.target_x = 0
                self.target_y = 0
            image = results[0].plot()

            logger.info('{}, {}'.format(int(self.target_x), int(self.target_y)))
            
        if show:
            cv2.imshow("detect_obj_yolov8", image)
            cv2.waitKey(1)

    def follow_line(self, show = 0):
        low = self.color_dist['black']['lower'] # 阈值设置
        high = self.color_dist['black']['high']
        img_fg = [None] * 9
        point = []
        image = self.image
        
        # 画面编号
        # 0  1  2
        # 3  4  5
        # 6  7  8

        # 分割图像
        img_fg[0] = image[0:160, 0:213]     # 左上
        img_fg[1] = image[0:160, 213:426]   # 中上
        img_fg[2] = image[0:160, 426:640]   # 右上
        img_fg[3] = image[160:320, 0:213]   # 左中
        img_fg[4] = image[160:320, 213:426] # 正中
        img_fg[5] = image[160:320, 426:640] # 右中
        img_fg[6] = image[320:480, 0:213]   # 左下
        img_fg[7] = image[320:480, 213:426] # 中下
        img_fg[8] = image[320:480, 426:640] # 右下

        # 画线区分画面
        cv2.line(image, (0, 160), (640, 160), (0, 200, 0), 1)
        cv2.line(image, (0, 320), (640, 320), (0, 200, 0), 1)
        cv2.line(image, (213, 0), (213, 480), (0, 200, 0), 1)
        cv2.line(image, (426, 0), (426, 480), (0, 200, 0), 1)

        for i, frame in enumerate(img_fg):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # 转换为HSV颜色空间
            mask = cv2.inRange(hsv, low, high) # 根据颜色范围进行二值化
            kernel = np.ones((5, 5), np.uint8) # 进行形态学操作，增加车道线宽度
            mask = cv2.dilate(mask, kernel)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 查找轮廓
            # 选择最大的车道线
            max_area = 0
            max_contour = None
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_contour = contour
            if max_contour is not None:
                moments = cv2.moments(max_contour)
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                point.append([1, cx, cy])
            else:
                point.append([0, 0, 0])
            i += 1
        if any(item[0] == 1 for item in point): # 有目标
            i_list = [item[0] for item in point]
            # 仿照红外循迹
            # 画面编号
            #   x->
            #         0 +213 +426
            # y   0   0   1    2
            # | +160  3   4    5
            #   +320  6   7    8
            if all(point[i][0] == 1 for i in [1, 4, 7]):
                cv2.circle(image, (point[1][1] + 213, point[1][2]), 5, (0, 0, 255), -1)
                self.target_x, self.target_y = point[1][1] + 213, point[1][2]
            elif all(point[i][0] == 1 for i in [4, 5, 7]):
                cv2.circle(image, (point[5][1] + 426, point[5][2] + 160), 5, (0, 0, 255), -1)
                self.target_x, self.target_y = point[5][1] + 426, point[5][2] + 160
            elif all(point[i][0] == 1 for i in [3, 4, 5]):
                cv2.circle(image, (point[5][1] + 426, point[5][2] + 160), 5, (0, 0, 255), -1)
                self.target_x, self.target_y = point[5][1] + 426, point[5][2] + 160
            elif all(point[i][0] == 1 for i in [4, 7]):
                cv2.circle(image, (point[4][1] + 213, point[4][2] + 160), 5, (0, 0, 255), -1)
                self.target_x, self.target_y = point[4][1] + 213, point[4][2] + 160
            else:
                self.target_x = self.target_y = 0

            logger.info('{}, {}'.format(int(self.target_x), int(self.target_y)))

        # 显示图像
        if show:
            cv2.imshow('Lane Detection', image)
            cv2.waitKey(1)