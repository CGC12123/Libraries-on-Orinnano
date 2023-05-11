from communite_module.Communications import SelfSerial
from Detections import Detections
from utils.SplitInt import get_high_low_data

from loguru import logger
import cv2
import os


if __name__ == '__main__':
    # cv与飞控通信口
    os.system("echo 123456 | sudo -S chmod 777 /dev/ttyUSB1")
    self_serial = SelfSerial('/dev/ttyUSB1')

    # 实例化检测类
    cap = cv2.VideoCapture(0)
    size = (640, 480)
    cap.set(3, size[0])
    cap.set(4, size[1])

    mode = 1

    logger.info('System Starting')
    while True:
        ret, image = cap.read()
        detection = Detections(image)
        if ret:
            mode = self_serial.uart_read_mode(mode)

            #发送上线消息
            if mode == 0:
                self_serial.uart_send_msg(0, (1, ))

            # 追色块
            elif mode == 1:
                detection.find_biggest_color('red')
                logger.info('{}, {}'.format(int(detection.target_x), int(detection.target_y)))
                msg = get_high_low_data(int(detection.target_x)) + get_high_low_data(int(detection.target_y))
                self_serial.uart_send_msg(32, msg) # 理应发出20 32为十六进制的20
            
    cap.release()
    cv2.destroyAllWindows()
