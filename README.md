# 📸 olv_camera_tpu_playground_py
A straightforward ROS 2 package written in Python, featuring multiple nodes to facilitate working with the Olive Camera, enhanced with TPU acceleration.

## 🚀 Apps 

### 0️⃣ Hello World App

This example is a simple parrot detector which you can test the hardware and make sure the Coral TPU is enabled. 

### 1️⃣ Object Recognition App
This example demonstrates object detection utilizing a ROS2 image topic and encases each detected object within a square.

![Object Detection Image](/images/object_recognition.gif "object_recognition.gif")

#### 📋 Object List
person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush.

🔗 **More Information**: [ObjectDetection.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/ObjectDetection.md)

### 2️⃣ Skeleton Detection App
Explore the utilization of the PoseNet model to detect human poses from a ROS2 image topic, pinpointing the location of body parts like elbows, shoulders, or feet.

![Skeleton Detection Image](/images/skeleton.gif "skeleton.gif")

#### 🚶‍♂️ Body Point List
nose, leftEye, rightEye, leftEar, rightEar, leftShoulder, rightShoulder, leftElbow, rightElbow, leftWrist, rightWrist, leftHip, rightHip, leftKnee, rightKnee, leftAnkle, rightAnkle.

🔗 **More Information**: [SkeletonDetection.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/SkeletonDetection.md)

### 3️⃣ Gesture Recognition App
An example showcasing the use of an MLP neural network model to train gesture classes.

![Gesture Recognition Image](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/2f1dda5e-51bc-43af-93a2-f22f5d41355b)

#### 📡 ROS2 Topic
The detection results will be published on the topic `/gesturerecognition`. Utilize `ros2 topic list` or `ros2 topic echo /gesturerecognition` to check whether a message is published, verifying the device’s operational status.

#### 🤏 Gestures
Both hands down, both hands up, left down / right up, right down / left up, left down / right side, right down / left side, hands on hip.

🔗 **More Information**: [GestureRecognition.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/GestureRecognition.md)

### 3️⃣ April Tag Detection App

![Skeleton Detection Image](/images/tag.gif "tag.gif")
