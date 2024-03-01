# Olive TPU Skeleton Detection v0.2

This is a Python script that performs skeleton detection using a TensorFlow Lite model running on an Edge TPU (Tensor Processing Unit) device. The script is designed to work with ROS2 (Robot Operating System 2) and receives compressed images from a camera topic. It then performs skeleton detection on the images using the TensorFlow Lite model and publishes the processed images with drawn keypoints and edges back to a different topic.

## Dependencies

- `rclpy`: ROS2 Python client library.
- `pycoral`: Python library for running TensorFlow Lite models on Edge TPUs.
- `svgwrite`: Python library for generating SVG files.
- `PIL`: Python Imaging Library for image processing.
- ROS2 message types: `CompressedImage`, `Imu`, `String`, and `Vector3`.

## Classes and Functions

### `AppNode`

- Inherits from `rclpy.node.Node`.
- Represents the main ROS2 node for skeleton detection.
- Initializes the node, creates subscriptions, and sets up the TensorFlow Lite model.

#### `__init__()`

- Constructor for the `AppNode` class.
- Initializes the ROS2 node with the name 'app_node_skeleton'.
- Creates a subscription to the '/olive/camera/owl1eye/image/compressed' topic to receive images from the camera.
- Creates a publisher on the '/olive/camera/owl1eye/tpu/compressed' topic to publish the compressed images with skeleton detection results.
- Sets up the TensorFlow Lite model for pose estimation.

#### `image_callback()`

- Callback function that gets executed when a new compressed image is received from the camera topic.
- Performs skeleton detection on the received image using the TensorFlow Lite model.
- Draws keypoints and edges on the image for detected poses.
- Publishes the processed image back to the '/olive/camera/owl1eye/tpu/compressed' topic.

## Constants and Global Variables

- `_NUM_KEYPOINTS`: The number of keypoints used in the pose estimation model (17 keypoints).
- `FILEPATH_POSE_MODEL_TPU`: The file path for the TensorFlow Lite model for pose estimation.

## Usage

1. Ensure that you have all the required dependencies installed (e.g., ROS2, pycoral, svgwrite, PIL, etc.).
2. Run the script. It will initialize the ROS2 node and wait for incoming images from the specified camera topic.
3. When an image is received, it will perform skeleton detection and publish the processed image with keypoints and edges to the specified topic.

Note: The script assumes that you have the necessary TensorFlow Lite model files (e.g., posenet_mobilenet_v1_075_353_481_quant_decoder_edgetpu.tflite) and test data (e.g., test_data/pose_model_thunder_uint8_tpu_edgetpu.tflite) available in the specified locations. Also, make sure that you have a connected Edge TPU device for pose estimation inference.
