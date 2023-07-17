from loguru import logger
import cv2
import os
import torch
import ultralytics

from communite_module.Communications import SelfSerial
from detection_module.Detections import Detections
from tools.SplitInt import get_high_low_data
from tools.GetKeyboardInput import transmit_keyboard_msg


if __name__ == '__main__':
    # cv与飞控通信口
    os.system("echo 123456 | sudo -S chmod 777 /dev/ttyUSB1")
    self_serial = SelfSerial('/dev/ttyUSB1')

    # 实例化检测类
    cap = cv2.VideoCapture(0)
    size = (640, 480)
    cap.set(3, size[0])
    cap.set(4, size[1])

    mode = 0

    # 加载模型
    # path1为yolov5配置文件路径
    # path2为yolov5模型文件
    path1 = '/home/c/Library/Cv_for_Orinnano/detection_module'
    path2 = '/home/c/Library/Cv_for_Orinnano/detection_module/models/yolov5n.pt'
    # model_v5 = torch.hub.load(path1, 'custom', path2, source='local', device = 0) # 不用的话注释掉提高启动效率
    # yolov8
    # model_v8 = ultralytics.YOLO("/home/c/Library/Cv_for_Orinnano/detection_module/models/yolov8n.pt") # 不用的话注释掉提高启动效率

    logger.info('System Starting')
    while True:
        ret, image = cap.read()
        detection = Detections(image)
        if ret:
            # 获取飞控指令
            mode = self_serial.uart_read_mode(mode)
            mode = 8
            #发送上线消息
            if mode == 0:
                self_serial.uart_send_msg(0, (1, ))

            # 键盘输入
            elif mode == 1:
                msg = transmit_keyboard_msg()
                if msg:
                    self_serial.uart_send_msg(0x01, msg)
                mode = 99

            # 追色块
            elif mode == 2:
                detection.find_biggest_color('red', show = 1)
                msg = get_high_low_data(int(detection.target_x)) + get_high_low_data(int(detection.target_y))
                self_serial.uart_send_msg(0x02, msg) 
            
            # 识别二维码或条形码
            elif mode == 3:
                detection.detect_qrcode(show = 0)

            # 字符识别
            elif mode == 4:
                detection.detect_character(character = 'A', show = 1)

            # 形状识别
            elif mode == 5:
                detection.detect_shape(mode = 'get shape', specify_color = 'red', target_shape = 'Circle', show = 1)

            # yolov5识别
            elif mode == 6:
                # detection.detect_obj_yolov5(model = model_v5, detect_target = 'person', show = 1)
                pass
            
            # yolov8识别
            elif mode == 7:
                # detection.detect_obj_yolov8(model = model_v8, detect_target = 'person', show = 1)
                pass
                
            elif mode == 8:
                detection.follow_line(show = 1)

            elif mode == 99:
                pass
            
    cap.release()
    cv2.destroyAllWindows()
