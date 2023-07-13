import os
import time
import subprocess

def T265_Start():
    sh1 = "/home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_1.sh"
    sh2s = ["echo 123456 | sudo -S chmod +x /home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_2.sh",
            "sudo chmod 777 /dev/ttyUSB0", 
            "/home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_2.sh"]
    sh2 = "bash -c '{}'".format("; ".join(sh2s))
    sh3 = "/home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_3.sh"

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], 
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)

    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh3, '--hold'], 
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)

if __name__ == '__main__':
    T265_Start()