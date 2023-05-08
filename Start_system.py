from utils.T265StartRos import T265_Start
import os
import subprocess

T265_Start()

subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', "python find_color.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)