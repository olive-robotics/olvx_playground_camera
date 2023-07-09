# olv_camera_tpu_playground_py
Simple python ROS 2 package with multiple nodes to start working with the Olive Camera with TPU acceleration. 

# Apps 

1) The object detection application
2) The skeleton detection applicaiton
3) The gesture detection application (using skeleton)

# 3- Gesture Recognition App

## ROS2 topic
The detection result will be published on the topic "/gesturerecognition"
With "ros2 topic list" or "ros2 topic echo /gesturerecognition" it can be checked whether a message is published to verify that the device is working.

## Gestures
The following gestures can be used by default

1) Both hands down
2) Both hands up
3) Left down / right up
4) Right down / left up


