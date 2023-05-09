'''
启动前双目重新拔插 可上电后再插入
USB0及USB1为两个ch340用于与飞控通信，其中一个走双目，一个走cv
'''
from utils.T265StartRos import T265_Start
import os
import subprocess

# 开新终端并执行双目启动程序
T265_Start()

# 执行cv
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', "echo 123456 | sudo -S chmod 777 /dev/ttyUSB1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
os.system("conda activate py37")
os.system("python /home/c/Library/Cv_for_Orinnano/find_color.py")