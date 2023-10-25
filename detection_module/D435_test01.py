import cv2
from loguru import logger
import numpy as np
from pyzbar import pyzbar
import pyrealsense2 as rs
import pytesseract
import torch
import sys 
import json
import math

def detect_obj_yolov5(depth_image, color_image, detect_target: str = None, model = None, show = 0):
    if model is not None:
        results = model(color_image)
        # 将结果转为json数据
        json_data = results.pandas().xyxy[0].to_json(orient="records")
        # 解析 JSON 数据
        target_x = 0
        target_y = 0
        depth = 0
        try:
            data = json.loads(json_data)
            for d in data:
                # 匹配目标
                if d.get('name') == detect_target and all(key in d for key in ('xmin', 'xmax', 'ymin', 'ymax')):
                    target_x = int((d['xmin'] + d['xmax']) / 2)
                    target_y = int((d['ymin'] + d['ymax']) / 2)
                    color_image = results.render()[0]
                    depth = depth_image[target_y, target_x]
                    break
                else:
                    target_x = 0
                    target_y = 0
                    depth = 0
        except:
            target_x = 0
            target_y = 0
            depth = 0
        logger.info('{}, {}, depth: {}'.format(int(target_x), int(target_y), depth))

    if show:
        cv2.imshow("detect_obj_yolov5", color_image)
        cv2.waitKey(1)

if __name__ == "__main__":
    path1 = '/home/c/Library/Cv_for_Orinnano/detection_module'
    path2 = '/home/c/Library/Cv_for_Orinnano/detection_module/models/yolov5n.pt'
    # model_land = torch.hub.load(path1, 'custom', path2_land, source='local', device = 0, force_reload = True) # 不用的话注释掉提高启动效率
    model = torch.hub.load(path1, 'custom', path2, source='local', device = 0, force_reload = True) # 不用的话注释掉提高启动效率
    
    # 配置RealSense深度相机
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

    # 启动深度和RGB流
    pipeline.start(config)

    while True:
        # 等待帧
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        # 将深度图像和RGB图像转换为numpy数组
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # 转化图像空间
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        detect_obj_yolov5(depth_image, color_image, detect_target = 'person', model = model, show = 1)