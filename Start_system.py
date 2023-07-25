'''
启动总入口
启动前双目重新拔插 可上电后再插入
USB0及USB1为两个ch340用于与飞控通信，其中0走双目，1走cv
'''
#!/bin/python
from tools.T265StartRos import T265_Start
from tools.CvStart import Cv_Start
import os
import subprocess
import time

time.sleep(10)

# 开新终端并执行双目启动程序
T265_Start()

# 执行cv
Cv_Start()
