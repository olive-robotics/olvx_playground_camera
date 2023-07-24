# Olive TPU Gesture Recognition MLP v1.0

This Python script performs gesture recognition using a TensorFlow Lite model running on an Edge TPU (Tensor Processing Unit) device. The script is designed to work with ROS2 (Robot Operating System 2) and receives compressed images from a camera topic. It then performs skeleton detection on the images using the TensorFlow Lite model and predicts the gestures made by the user.

## Dependencies

- `rclpy`: ROS2 Python client library.
- `pycoral`: Python library for running TensorFlow Lite models on Edge TPUs.
- `svgwrite`: Python library for generating SVG files.
- `PIL`: Python Imaging Library for image processing.
- `pandas`: Python library for data manipulation and analysis.
- `sklearn`: Python library for machine learning.
- `joblib`: Python library for serialization of Python objects.
- `numpy`: Python library for numerical computing.
- `tflite_runtime`: TensorFlow Lite runtime for Python.
- ROS2 message types: `CompressedImage`, `Imu`, `String`, and `Vector3`.

## Classes and Functions

### `AppNode`

- Inherits from `rclpy.node.Node`.
- Represents the main ROS2 node for gesture recognition.
- Initializes the node, sets up the TensorFlow Lite model, and loads the pre-trained MLP model and label encoder.

#### `__init__()`

- Constructor for the `AppNode` class.
- Initializes the ROS2 node with the name 'app_node_skeleton'.
- Loads the pre-trained MLP model and label encoder for gesture recognition.
- Creates a subscription to the '/olive/camera/x1687477489523/image/compressed' topic to receive images from the camera.
- Creates publishers for the compressed images with skeleton detection results and the predicted gestures.

#### `trainMLP()`

- Function to train the MLP model for gesture recognition.
- Reads data from the 'test_data/data2.txt' text file.
- Converts labels into numerical form using the label encoder.
- Splits the data into training and testing sets.
- Defines the MLP model and trains it using the training data.
- Evaluates the model and prints the accuracy.
- Saves the trained model and label encoder using joblib.

#### `image_callbackTest()`

- Callback function that gets executed when a new compressed image is received from the camera topic.
- Performs skeleton detection on the received image using the TensorFlow Lite model.
- Predicts the gesture made by the user using the trained MLP model and label encoder.
- Publishes the processed image with drawn keypoints and edges to the specified topic.
- Publishes the predicted gesture to the '/olive/camera/owl1eye/tpu/gesture' topic.

#### `image_callback()`

- Callback function for collecting data for training the MLP model.
- Performs skeleton detection on the received image using the TensorFlow Lite model.
- If all keypoints are detected (17 keypoints), the x and y coordinates of each keypoint are collected and saved to the 'test_data/data2.txt' text file along with the gesture label '7'.

## Usage

1. Ensure that you have all the required dependencies installed (e.g., ROS2, pycoral, svgwrite, PIL, pandas, scikit-learn, joblib, numpy, tflite_runtime, etc.).
2. To train the MLP model for gesture recognition, uncomment the `self.trainMLP()` line in the `__init__()` function and run the script. This step should be performed once before performing gesture recognition.
3. After training the MLP model, comment out the `self.trainMLP()` line again and run the script. It will initialize the ROS2 node and wait for incoming images from the specified camera topic.
4. When an image is received, it will perform skeleton detection, predict the gesture, and publish the processed image with keypoints and edges to the specified topic.
5. The predicted gesture will also be published to the '/olive/camera/owl1eye/tpu/gesture' topic.

Note: The script assumes that you have the necessary TensorFlow Lite model files (e.g., posenet_mobilenet_v1_075_353_481_quant_decoder_edgetpu.tflite) and test data (e.g., test_data/data2.txt) available in the specified locations. Also, make sure that you have a connected Edge TPU device for gesture recognition inference.

Please note that this documentation is generated based on the code provided up to my knowledge cutoff date in September 2021. If there have been any updates or changes to the code or dependencies after this date, they will not be reflected here.
