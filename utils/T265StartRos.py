import os
import time

os.system("chmod +x ./bash/T265_Start_1.sh")
os.system("./bash/T265_Start_1.sh")
time.sleep(3)

os.system("xterm -e 'chmod +x ./bash/T265_Start_2.sh'")
os.system("./bash/T265_Start_2.sh")
time.sleep()

os.system("xterm -e 'chmod +x ./bash/T265_Start_3.sh'")
os.system("./bash/T265_Start_3.sh")