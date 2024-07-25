# 📸 olvx_playground_camera
A straightforward ROS 2 package written in Python, featuring multiple nodes to facilitate working with the Olive Camera, enhanced with TPU acceleration.

The camera uses the default internal calibration file. If you want to recalibrate your camera, please follow the steps outlined in the documentation.

https://docs.olive-robotics.com/hardware/camera/camera_01_tp.html#camera-calibration

## Supported Embedded Libraries for the Olive AI Camera

| Coral | OpenCV | ROS 2 | Python 3 |
| ----- | ------ | ----- | -------  |
| ![1](/images/coral2.png "1.png") | ![2](/images/opencvlogo3.png "2.png")| ![3](/images/ros2.png "3.png") | ![4](/images/python2.png "4.png") |

## 🚀 Apps 

### 0️⃣ Hello World App (TPU Embedded App)

This example is a simple parrot detector which you can test the hardware and make sure the Coral TPU is enabled. 

Sample output:

```
Olive TPU Hello World v0.1
step1
step2
step3
step4
Ara macao (Scarlet Macaw): 0.75781
```

### 1️⃣ Object Recognition (TPU Embedded App)
This example demonstrates object detection utilizing a ROS2 image topic and encases each detected object within a square.

![Object Detection Image](/images/object_recognition.gif "object_recognition.gif")

```
python3 app_node_object_detection.py
```

#### 📋 Object List
person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush.

🔗 **More Information**: [ObjectDetection.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/ObjectDetection.md)

### 2️⃣ Skeleton Detection (TPU Embedded App)
Explore the utilization of the PoseNet model to detect human poses from a ROS2 image topic, pinpointing the location of body parts like elbows, shoulders, or feet.

![Skeleton Detection Image](/images/skeleton.gif "skeleton.gif")

```
python3 app_node_skeleton_posenet.py
```

#### 🚶‍♂️ Body Point List
nose, leftEye, rightEye, leftEar, rightEar, leftShoulder, rightShoulder, leftElbow, rightElbow, leftWrist, rightWrist, leftHip, rightHip, leftKnee, rightKnee, leftAnkle, rightAnkle.

🔗 **More Information**: [SkeletonDetection.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/SkeletonDetection.md)

### 3️⃣ Gesture Recognition (TPU Embedded App)
An example showcasing the use of an MLP neural network model to train gesture classes.

![Gesture Recognition Image](https://github.com/olive-robotics/olv_camera_tpu_playground_py/assets/5897501/2f1dda5e-51bc-43af-93a2-f22f5d41355b)

#### 📡 ROS2 Topic
The detection results will be published on the topic `/gesturerecognition`. Utilize `ros2 topic list` or `ros2 topic echo /gesturerecognition` to check whether a message is published, verifying the device’s operational status.

#### 🤏 Gestures
Both hands down, both hands up, left down / right up, right down / left up, left down / right side, right down / left side, hands on hip.

🔗 **More Information**: [GestureRecognition.md](https://github.com/olive-robotics/olv_camera_tpu_playground_py/blob/main/GestureRecognition.md)

### 4️⃣ April Tag Detection (CPU Embedded App)

![Skeleton Detection Image](/images/tag.gif "tag.gif")

Example forked from:
https://github.com/ros-misc-utilities/apriltag_detector

A4 Tag Dataset:
https://github.com/rgov/apriltag-pdfs

Download the OpenCV-4 Compiled for Olive Camera
[Download](https://drive.google.com/file/d/1AaO6qKZIV1wDaI-2pzJ3npGFW7vGyhDP/view?usp=sharing)

Place the folder in the home and follow this namings:

```
/home/olive/opencv_install/opencv-4.x/
```

Update the .bashrc and add this lines to it:

```
source /opt/olive/script/env.sh
export PATH="/home/olive/.local/bin:$PATH"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/olive/opencv_install/opencv-4.x/build/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/olive/lib
export OpenCV_DIR=/home/olive/opencv_install/opencv-4.x/build
export PYTHONPATH=~/opencv_install/opencv-4.x/build/lib/python3:$PYTHONPATH
```

Then install the AprilTag 3 library from examples/04-AprilTag/lib/apriltag

```
rm -r build
cmake -B build -DCMAKE_BUILD_TYPE=Release
sudo cmake --build build --target install
```

Then build the ROS2 project from examples/04-AprilTag/lib/workspace. You can skip also building if you don't want to change the code.

```
source install/setup.bash
colcon build
```

Then run it with:

```
ros2 launch apriltag_detector node.launch.py
```

### 5️⃣ OpenCV Examples (Edge Dector, Optical Flow, Rectify, IMShow) (Host Computer App)

Run this example on your host computer. Compatible with CPU and GPU.

```
python3 edge_detector.py
```

![Skeleton Detection Image](/images/opencv.png "opencv.png")

### 6️⃣ Monocular Depth Estimation (Host Computer App)

Run this example on your host computer. Compatible with CPU and GPU.

```
python3 depth_estimation.py
```

![Skeleton Detection Image](/images/MonocularMiDaSGIF.gif "depth.gif")

