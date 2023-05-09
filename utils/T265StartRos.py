import os
import time
import subprocess

def T265_Start():
    sh1 = "/home/c/Library/Cv_for_Orinnano/utils/bash/T265_Start_1.sh"
    sh2_1 = "echo 123456 | sudo -S chmod +x /home/c/Library/Cv_for_Orinnano/utils/bash/T265_Start_2.sh"
    sh2_2 = "/home/c/Library/Cv_for_Orinnano/utils/bash/T265_Start_2.sh"
    sh3 = "/home/c/Library/Cv_for_Orinnano/utils/bash/T265_Start_3.sh"

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(3)

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2_1, '--hold'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.system(sh2_2)

    time.sleep(3)

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh3, '--hold'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(3)

T265_Start()