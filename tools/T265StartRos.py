import os
import time
import subprocess
import threading

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

def T265_Start_Thread1():
    os.system("/home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_1.sh")

def T265_Start_Thread2():
    os.system("echo 123456 | sudo -S chmod +x /home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_2.sh")
    os.system("sudo chmod 777 /dev/ttyUSB0")
    os.system("/home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_2.sh")

def T265_Start_Thread3():
    os.system("/home/c/Library/Cv_for_Orinnano/tools/bash/T265_Start_3.sh")

def T265_ThreadStart():
    # 创建线程对象
    thread1 = threading.Thread(target=T265_Start_Thread1)
    thread2 = threading.Thread(target=T265_Start_Thread2)
    thread3 = threading.Thread(target=T265_Start_Thread3)

    thread1.start()
    time.sleep(5)
    thread2.start()
    time.sleep(5)
    thread3.start()
    time.sleep(5)

    # 等待线程结束
    thread1.join()
    thread2.join()
    thread3.join()

if __name__ == '__main__':
    # T265_Start()
    T265_ThreadStart()