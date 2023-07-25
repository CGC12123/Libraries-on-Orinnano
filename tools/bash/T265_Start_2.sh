#!/bin/bash

source /home/c/Library/acfly_ws/devel/setup.bash
echo 123456 | sudo -S chmod 777 /dev/ttyAMA0
roslaunch mavros acfly.launch fcu_url:=/dev/ttyUSB0:57600