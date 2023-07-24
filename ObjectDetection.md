# Olive TPU Object Detection v0.2

This is a Python script that performs object detection using a TensorFlow Lite model running on an Edge TPU (Tensor Processing Unit) device. The script is designed to work with ROS2 (Robot Operating System 2) and receives images from a camera topic, performs object detection on the images using the TensorFlow Lite model, and publishes the detected objects back to a different topic as compressed images with bounding boxes and labels.

## Dependencies

- `rclpy`: ROS2 Python client library.
- `pycoral`: Python library for running TensorFlow Lite models on Edge TPUs.
- `PIL`: Python Imaging Library for image processing.
- ROS2 message types: `CompressedImage`, `Imu`, `String`, and `Vector3`.

## Classes and Functions

### `AppNode`

- Inherits from `rclpy.node.Node`.
- Represents the main ROS2 node for object detection.
- Initializes the node, creates subscriptions, and sets up the TensorFlow Lite model.

#### `__init__()`

- Constructor for the `AppNode` class.
- Initializes the ROS2 node with the name 'app_node'.
- Creates a subscription to the '/olive/camera/x1687477489523/image/compressed' topic to receive images from the camera.
- Creates a publisher on the '/olive/one/tpu/compressed' topic to publish the compressed images with object detection results.
- Sets up the TensorFlow Lite model and loads the labels.

#### `image_callback()`

- Callback function that gets executed when a new compressed image is received from the camera topic.
- Performs object detection on the received image using the TensorFlow Lite model.
- Draws bounding boxes and labels on the image for detected objects.
- Publishes the processed image back to the '/olive/one/tpu/compressed' topic.

#### `simple_test()`

- A standalone function that demonstrates a simple test using a different TensorFlow Lite model (mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite).
- This function is not directly used in the main script.

### `main()`

- Entry point of the script.
- Initializes the ROS2 context and creates the `AppNode` instance.
- Spins the ROS2 node to start processing messages.
- When the node is shutdown, it cleans up and shuts down the ROS2 context.

## Usage

1. Make sure you have all the required dependencies installed (e.g., ROS2, pycoral, etc.).
2. Run the script. It will initialize the ROS2 node and wait for incoming images from the specified camera topic.
3. When an image is received, it will perform object detection and publish the processed image to the specified topic with bounding boxes and labels.

Note: Ensure that the TensorFlow Lite model files (e.g., ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite) and label files (e.g., coco_labels.txt) are available in the appropriate locations as specified in the script. The script may also require a connected Edge TPU device for object detection inference.
