# 📸 olv_camera_tpu_playground_py
A straightforward ROS 2 package written in Python, featuring multiple nodes to facilitate working with the Olive Camera, enhanced with TPU acceleration.

## 🚀 Apps 

### 1️⃣ Object Recognition App
This example demonstrates object detection utilizing a ROS2 image topic and encases each detected object within a square.

![Object Detection Image](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/166cda6f-37e7-43a0-8ac1-754c82cbd4dd)

#### 📋 Object List
* person
* bicycle
* car
* [More...]

🔗 **More Information**: [ObjectDetection.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/ObjectDetection.md)

### 2️⃣ Skeleton Detection App
Explore the utilization of the PoseNet model to detect human poses from a ROS2 image topic, pinpointing the location of body parts like elbows, shoulders, or feet.

![Skeleton Detection Image](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/15bbbcb8-b523-4865-ada3-1ff0c2396023)

#### 🚶‍♂️ Body Point List
0) nose
1) leftEye
2) rightEye
[More...]

🔗 **More Information**: [SkeletonDetection.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/SkeletonDetection.md)

### 3️⃣ Gesture Recognition App
An example showcasing the use of an MLP neural network model to train gesture classes.

![Gesture Recognition Image](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/2f1dda5e-51bc-43af-93a2-f22f5d41355b)

#### 📡 ROS2 Topic
The detection results will be published on the topic `/gesturerecognition`. Utilize `ros2 topic list` or `ros2 topic echo /gesturerecognition` to check whether a message is published, verifying the device’s operational status.

#### 🤏 Gestures
The default usable gestures include:

1) Both hands down
2) Both hands up
3) Left down / right up
[More...]

🔗 **More Information**: [GestureRecognition.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/GestureRecognition.md)
