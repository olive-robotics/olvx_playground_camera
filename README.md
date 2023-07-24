# olv_camera_tpu_playground_py
Simple python ROS 2 package with multiple nodes to start working with the Olive Camera with TPU acceleration. 

# Apps 

# 1- Object Recognition App
An example that performs object detection with a ROS2 image topic and draws a square around each object. 

![img_object_detection](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/166cda6f-37e7-43a0-8ac1-754c82cbd4dd)

### Object List
* person
* bicycle
* car
* motorcycle
* airplane
* bus
* train
* truck
* boat
* traffic light
* fire hydrant
* stop sign
* parking meter
* bench
* bird
* cat
* dog
* horse
* sheep
* cow
* elephant
* bear
* zebra
* giraffe
* backpack
* umbrella
* handbag
* tie
* suitcase
* frisbee
* skis
* snowboard
* sports ball
* kite
* baseball bat
* baseball glove
* skateboard
* surfboard
* tennis racket
* bottle
* wine glass
* cup
* fork
* knife
* spoon
* bowl
* banana
* apple
* sandwich
* orange
* broccoli
* carrot
* hot dog
* pizza
* donut
* cake
* chair
* couch
* potted plant
* bed
* dining table
* toilet
* tv
* laptop
* mouse
* remote
* keyboard
* cell phone
* microwave
* oven
* toaster
* sink
* refrigerator
* book
* clock
* vase
* scissors
* teddy bear
* hair drier
* toothbrush

More Information:
https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/ObjectDetection.md

# 2- Skeleton Detection App
An example showing how to use the PoseNet model to detect human poses from ROS2 image topic, such as locating the position of someone’s elbow, shoulder or foot.

![img_skeleton_detection](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/15bbbcb8-b523-4865-ada3-1ff0c2396023)

### Body point list
0)	nose
1)	leftEye
2)	rightEye
3)	leftEar
4)	rightEar
5)	leftShoulder
6)	rightShoulder
7)	leftElbow
8)	rightElbow
9)	leftWrist
10)	rightWrist
11)	leftHip
12)	rightHip
13)	leftKnee
14)	rightKnee
15)	leftAnkle
16)	rightAnkle

More Information:
https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/SkeletonDetection.md

# 3- Gesture Recognition App
An exmaple of showing how to use MLP neural network model to train gesture classes.

![img_gesture_recognition](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/2f1dda5e-51bc-43af-93a2-f22f5d41355b)

### ROS2 topic
The detection result will be published on the topic "/gesturerecognition"
With "ros2 topic list" or "ros2 topic echo /gesturerecognition" it can be checked whether a message is published to verify that the device is working.

### Gestures
The following gestures can be used by default

1) Both hands down
2) Both hands up
3) Left down / right up
4) Right down / left up
5) Left down / right side
6) Right down / left side
7) Hands on hip

More Information:
https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/GestureRecognition.md
