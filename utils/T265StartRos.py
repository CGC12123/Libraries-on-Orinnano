import os
import time
import subprocess

def T265_Start():
    sh1 = "./bash/T265_Start_1.sh"
    sh2_1 = "echo 123456 | sudo -S chmod -x ./bash/T265_Start_2.sh"
    sh2_2 = "./bash/T265_Start_2.sh"
    sh3 = "./bash/T265_Start_3.sh"

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(3)

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2_1], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.system(sh2_2)

    time.sleep(3)

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh3], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)