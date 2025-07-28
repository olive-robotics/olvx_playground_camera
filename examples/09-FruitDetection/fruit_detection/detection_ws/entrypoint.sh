#!/usr/bin/bash

source /opt/ros/humble/setup.sh
source /root/detection_ws/install/setup.sh

ros2 launch fruit_detection fruit_detection.launch.py
