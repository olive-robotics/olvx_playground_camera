# ROS2 libraries
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy, LivelinessPolicy
from cv_bridge import CvBridge
from tensorflow.lite.python.interpreter import Interpreter
# Additional libraries
from enum import Enum
import numpy as np
import cv2
from dataclasses import dataclass
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# ------------------------ From utils_hitnet ------------------------
class ModelType(Enum):
    eth3d = 0
    middlebury = 1
    flyingthings = 2


@dataclass
class CameraConfig:
    baseline: float
    f: float


# ------------------------ From HitNet ------------------------
class HitNet():
    def __init__(self, model_path, model_type=ModelType.eth3d, camera_config=CameraConfig(0.150, 1920 * (2.8 / 6.8)),
                 use_tflite=True):
        self.model_path = model_path
        self.model_type = model_type
        self.camera_config = camera_config
        self.use_tflite = use_tflite

        if use_tflite:
            # Load the TFLite model
            self.interpreter = Interpreter(model_path=model_path, num_threads=4)
            self.interpreter.allocate_tensors()

            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        else:
            # Load the SavedModel
            self.model = tf.saved_model.load(model_path)

    def __call__(self, left_img, right_img):
        disparity_map = self.estimate_disparity(left_img, right_img)
        return self.get_depth(disparity_map)

    def prepare_input(self, left_img, right_img):
        if self.use_tflite:
            left_img = cv2.resize(left_img, (256, 256))
            right_img = cv2.resize(right_img, (256, 256))

        if (self.model_type == ModelType.eth3d):
            # Shape (1, None, None, 2)
            left_img = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
            right_img = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

            left_img = np.expand_dims(left_img, 2)
            right_img = np.expand_dims(right_img, 2)
            combined_img = np.concatenate((left_img, right_img), axis=-1) / 255.0
        else:
            # Shape (1, None, None, 6)
            left_img = cv2.cvtColor(left_img, cv2.COLOR_BGR2RGB)
            right_img = cv2.cvtColor(right_img, cv2.COLOR_BGR2RGB)
            combined_img = np.concatenate((left_img, right_img), axis=-1) / 255.0

        return tf.convert_to_tensor(np.expand_dims(combined_img, 0), dtype=tf.float32)

    def get_depth(self, disparity_map):
        return (self.camera_config.f * self.camera_config.baseline) / disparity_map

    def draw_disparity(self, disparity_map):
        diff = np.max(disparity_map) - np.min(disparity_map)

        # Check if the disparity_map is constant
        if diff == 0:
            norm_disparity_map = np.zeros_like(disparity_map, dtype=np.uint8)
        else:
            norm_disparity_map = (255 * ((disparity_map - np.min(disparity_map)) / diff)).astype(np.uint8)

        return cv2.applyColorMap(cv2.convertScaleAbs(norm_disparity_map, 1), cv2.COLORMAP_JET)

    def draw_depth(self, depth_map, max_dist):
        norm_depth_map = 255 * (1 - depth_map / max_dist)
        norm_depth_map[norm_depth_map < 0] = 0
        norm_depth_map[depth_map == 0] = 0
        return cv2.applyColorMap(cv2.convertScaleAbs(norm_depth_map, 1), cv2.COLORMAP_JET)

    def estimate_disparity(self, left_img, right_img):
        try:
            input_tensor = self.prepare_input(left_img, right_img)
        except ValueError as e:
            print(f"Error preparing input: {str(e)}")
            return None

        if self.use_tflite:
            # Run inference with the TFLite model
            self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
            self.interpreter.invoke()
            disparity_map = self.interpreter.get_tensor(self.output_details[0]['index'])
        else:
            # Run inference with the SavedModel
            print(self.model.signatures.keys())
            output_tensor = self.model.signatures['serving_default'](input_tensor)['reference_output_disparity:0']
            disparity_map = output_tensor.numpy()
        if self.model_type == ModelType.flyingthings:
            left_disparity, right_disparity = disparity_map
            self.disparity_map = left_disparity
        else:
            self.disparity_map = disparity_map

        return disparity_map


# ------------------------ ROS2 Node ------------------------
class StereoDepthProcessor(Node):
    def __init__(self):
        super().__init__('stereo_image_processor')
        self.bridge = CvBridge()

        # Initialize the model
        model_path = "saved_model_256x256/model_float32.tflite"
        model_type = ModelType.eth3d
        camera_config = CameraConfig(baseline=0.05, f=707)
        self.hitnet = HitNet(model_path, model_type, camera_config)

        # Publishers for the depth map and disparity map
        self.depth_pub = self.create_publisher(Image, 'stereo_depth_map', qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.disparity_pub = self.create_publisher(Image, 'stereo_disparity_map', qos_profile=rclpy.qos.qos_profile_sensor_data)

        # Subscribe to the left and right image topics
        self.left_img = None
        self.right_img = None
        # self.left_sub = self.create_subscription(CompressedImage, '/olive/one/camera/compressed', self.process_left_image, qos_profile=rclpy.qos.qos_profile_sensor_data)
        # self.right_sub = self.create_subscription(CompressedImage, '/olive/right/camera/compressed', self.process_right_image, qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.left_sub = self.create_subscription(CompressedImage, '/olive/camera/eye2/image/compressed', self.process_left_image,
                                                 qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.right_sub = self.create_subscription(CompressedImage, '/olive/camera/eye1/image/compressed', self.process_right_image,
                                                  qos_profile=rclpy.qos.qos_profile_sensor_data)

    def process_left_image(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        # Decompress the image using OpenCV
        self.left_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.get_logger().info('Left Image received')
        #self.left_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        self.process_images()

    def process_right_image(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        # Decompress the image using OpenCV
        self.right_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.get_logger().info('Right Image received')
        #self.right_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        self.process_images()

    def process_images(self):
        if self.left_img is not None and self.right_img is not None:
            disparity_map = self.hitnet(self.left_img, self.right_img)
            disparity_map = disparity_map[0, :, :, 0]
            #self.get_logger().info('disparity_map shape:{}'.format(disparity_map.shape))
            depth_map = self.hitnet.get_depth(disparity_map)
            disparity_img = self.hitnet.draw_disparity(disparity_map)
            #self.get_logger().info('depth_map maximum value:{}'.format(np.max(depth_map)))
            depth_img = self.hitnet.draw_depth(depth_map, max_dist=40)
            disparity_msg = self.bridge.cv2_to_imgmsg(disparity_img, "bgr8")
            depth_msg = self.bridge.cv2_to_imgmsg(depth_img, "bgr8")
            self.disparity_pub.publish(disparity_msg)
            self.depth_pub.publish(depth_msg)
            # Reset the images
            #self.left_img = None
            #self.right_img = None


def main(args=None):
    rclpy.init()
    node = StereoDepthProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
