'''
启动总入口
启动前双目重新拔插 可上电后再插入
USB0及USB1为两个ch340用于与飞控通信，其中0走双目，1走cv
'''
from utils.T265StartRos import T265_Start
import os
import subprocess

# 开新终端并执行双目启动程序
T265_Start()

# 执行cv
cv_shs = ["python /home/c/Library/Cv_for_Orinnano/Cv_mode.py"]
cv_sh = "bash -c '{}'".format("; ".join(cv_shs))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', cv_sh], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# os.system("export PATH=/home/c/archiconda3/bin:$PATH")
# os.system("source ~/.bashrc")
# os.system("condaenv")
# os.system("conda activate py37")
# os.system("python /home/c/Library/Cv_for_Orinnano/Cv_Mode.py")