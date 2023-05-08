from utils.T265StartRos import T265_Start
import os
import subprocess

os.system("echo 123456 | sudo -S chmod 777 /dev/ttyUSB0")
T265_Start()

subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', "python /home/c/Library/Cv_for_Orinnano/find_color.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)