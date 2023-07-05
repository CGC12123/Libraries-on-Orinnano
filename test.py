from loguru import logger
import cv2
import os

from detection_module.Detections import Detections
from tools.SplitInt import get_high_low_data
import torch

    # cv与飞控通信口

    # 实例化检测类

path1 = '/home/c/Library/Cv_for_Orinnano/detection_module/'
path2 = '/home/c/Library/Cv_for_Orinnano/detection_module/models/yolov5n.pt'
model = torch.hub.load(path1, 'custom', path2, source='local', device = 0)
    # detection.detect_obj_yolo(show = 1)
            
    # cap.release()
    # cv2.destroyAllWindows()
