import os
import time
import subprocess

sh1 = "./bash/T265_Start_1.sh"
sh2 = "./bash/T265_Start_2.sh"
sh3 = "./bash/T265_Start_3.sh"

subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c', sh1])
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c', sh2])
subprocess.Popen(['gnome-terminal', '-x', 'bash', '-c', sh3])

# time.sleep(3)

# os.system("open -a Terminal")
# os.system("chmod +x ./bash/T265_Start_2.sh")
# os.system("./bash/T265_Start_2.sh")
# # time.sleep(3)

# os.system("open -a Terminal")
# os.system("chmod +x ./bash/T265_Start_3.sh")
# os.system("./bash/T265_Start_3.sh")