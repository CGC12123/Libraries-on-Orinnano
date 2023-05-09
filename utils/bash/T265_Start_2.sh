#!/bin/bash
 
echo 123456 | sudo -S chmod 777 /dev/ttyAMA0
roslaunch mavros acfly.launch fcu_url:=/dev/ttyUSB0:57600