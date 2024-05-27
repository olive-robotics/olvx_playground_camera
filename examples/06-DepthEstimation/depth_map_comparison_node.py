from sklearn.metrics import mean_squared_error
from skimage.metrics import structural_similarity as ssim
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import Image
from message_filters import ApproximateTimeSynchronizer, Subscriber
from cv_bridge import CvBridge
from my_camera_subscriber.camera_subscriber import MonoDepthEstimator
import cv2
import numpy as np
import tensorflow as tf
from tflite_runtime.interpreter import Interpreter, load_delegate
import tflite_runtime.interpreter as tflite
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common
from pycoral.adapters import classify
import time

from message_filters import ApproximateTimeSynchronizer, Subscriber

class DepthMapComparisonNode(Node):
    def __init__(self):
        super().__init__('depth_map_comparison')
        self.midas_estimator = MonoDepthEstimator('GPU')  # or 'GPU' or 'TPU'
        self.bridge = CvBridge()

        # Create subscribers for the image and depth map topics
        self.image_sub = Subscriber(self, Image, '/d455_1_rgb_image')
        self.depth_map_sub = Subscriber(self, Image, '/d455_1_depth_image')
        # Create a publisher for the depth map
        self.depth_map_publisher = self.create_publisher(Image, '/midas_depth_map', 1)

        # Create an ApproximateTimeSynchronizer to synchronize the image and depth map topics
        self.ats = ApproximateTimeSynchronizer([self.image_sub, self.depth_map_sub], queue_size=10, slop=0.4)
        self.ats.registerCallback(self.callback)

    def callback(self, image_msg, depth_map_msg):
        midas_depth_map = self.process_image(image_msg)
        # Convert the depth map to grayscale
        midas_depth_map_gray = cv2.cvtColor(midas_depth_map, cv2.COLOR_BGR2GRAY)
        # Convert the grayscale depth map to a ROS Image message
        depth_map_msg = self.bridge.cv2_to_imgmsg(midas_depth_map_gray, encoding='mono8')
        # Publish the depth map
        self.depth_map_publisher.publish(depth_map_msg)
        ground_truth_depth_map = self.bridge.imgmsg_to_cv2(depth_map_msg, desired_encoding='passthrough')
        # Compare the depth maps
        self.compare_depth_maps(midas_depth_map, ground_truth_depth_map)



    def process_image(self, msg):
        """
        The function processes the input image from the NVIDIA dataset and returns the depth_map

        Args:
            msg (Image): The image data message

        Returns:
            depth_map: The depth map
        """
        # Convert the ROS Image message to an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # Convert the image to RGB format
        img_rgb = cv_image / 255.0
        # Resize the image to 256x256 pixels
        img_resized = tf.image.resize(img_rgb, [256,256], method='bicubic', preserve_aspect_ratio=False)
        # Normalize the pixel values
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        img_input = (img_resized.numpy() - mean) / std
        reshape_img = img_input.reshape(1,256,256,3)
        tensor = tf.convert_to_tensor(reshape_img, dtype=tf.float32)

        # Run inference on the input tensor using the MiDaS21 model
        common.set_input(self.midas_estimator.interpreter, tensor)
        self.midas_estimator.interpreter.invoke()
        output = common.output_tensor(self.midas_estimator.interpreter, 0)
        prediction = output.reshape(256, 256)
        # Resize the depth map to the original image size
        prediction = cv2.resize(prediction, (cv_image.shape[1], cv_image.shape[0]), interpolation=cv2.INTER_CUBIC)
        depth_min = prediction.min()
        depth_max = prediction.max()
        depth_map = (255 * (prediction - depth_min) / (depth_max - depth_min)).astype("uint8")
        depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)

        return depth_map

    """def image_callback(self, msg):
        self.latest_image_msg = msg
    def timer_callback(self):
        if self.latest_image_msg is not None:
            midas_depth_map = self.process_image(self.latest_image_msg)
            # Convert the depth map to grayscale
            midas_depth_map_gray = cv2.cvtColor(midas_depth_map, cv2.COLOR_BGR2GRAY)
            # Convert the grayscale depth map to a ROS Image message
            depth_map_msg = self.bridge.cv2_to_imgmsg(midas_depth_map_gray, encoding='mono8')
            # Publish the depth map
            self.depth_map_publisher.publish(depth_map_msg)
            if self.latest_depth_map is not None:
                self.compare_depth_maps(midas_depth_map, self.latest_depth_map)"""
    def calculate_metrics(self, depth_map1, depth_map2):
        # Ensure the depth maps are floating point values
        depth_map1 = depth_map1.astype(np.float32)
        depth_map2 = depth_map2.astype(np.float32)
        # Add a small constant to the depth maps to prevent division by zero
        depth_map1 += 1e-6
        depth_map2 += 1e-6
        # Calculate the absolute relative difference
        ard = np.mean(np.abs(depth_map1 - depth_map2) / depth_map2)

        # Calculate the squared relative difference
        srd = np.mean(((depth_map1 - depth_map2) ** 2) / depth_map2)

        # Calculate the root mean squared error
        rmse = np.sqrt(mean_squared_error(depth_map1, depth_map2))

        # Calculate the log10 error
        log10_error = np.mean(np.abs(np.log10(depth_map1) - np.log10(depth_map2)))

        # Calculate the delta values
        ratio = depth_map1 / depth_map2
        delta_125 = np.mean(ratio < 1.25)
        delta_125_2 = np.mean(ratio < 1.25 ** 2)
        delta_125_3 = np.mean(ratio < 1.25 ** 3)
        return ard, srd, rmse, log10_error, delta_125, delta_125_2, delta_125_3
    def depth_map_callback(self, msg):
        self.latest_depth_map = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    def compare_depth_maps(self, depth_map1, depth_map2):
        # Convert color depth maps to grayscale
        depth_map1_gray = cv2.cvtColor(depth_map1, cv2.COLOR_BGR2GRAY)
        if len(depth_map2.shape) == 3 and depth_map2.shape[2] == 3:
            depth_map2_gray = cv2.cvtColor(depth_map2, cv2.COLOR_BGR2GRAY)
        else:
            depth_map2_gray = depth_map2
        depth_map2_gray_resized = cv2.resize(depth_map2_gray, (depth_map1_gray.shape[1], depth_map1_gray.shape[0]), interpolation=cv2.INTER_CUBIC)
        depth_map1_gray = depth_map1_gray.astype(np.float32)
        depth_map2_gray_resized = depth_map2_gray_resized.astype(np.float32)

        # Calculate the metrics
        ard, srd, rmse, log10_error, delta_125, delta_125_2, delta_125_3 = self.calculate_metrics(depth_map1_gray, depth_map2_gray_resized)

        self.get_logger().info(f'ARD: {ard}')
        self.get_logger().info(f'SRD: {srd}')
        self.get_logger().info(f'RMSE: {rmse}')
        self.get_logger().info(f'Log10 Error: {log10_error}')
        self.get_logger().info(f'δ < 1.25: {delta_125}')
        self.get_logger().info(f'δ < 1.25²: {delta_125_2}')
        self.get_logger().info(f'δ < 1.25³: {delta_125_3}')


def main(args=None):
    rclpy.init(args=args)
    depth_map_comparison_node = DepthMapComparisonNode()
    # Use a multithreaded executor to process callbacks
    executor = MultiThreadedExecutor(num_threads=1)
    executor.add_node(depth_map_comparison_node)
    try:
        executor.spin()
    finally:
        # Shutdown the node and executor
        executor.shutdown()
        depth_map_comparison_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
