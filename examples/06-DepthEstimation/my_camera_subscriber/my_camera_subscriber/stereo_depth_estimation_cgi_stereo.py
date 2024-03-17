# ROS2 libraries
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
# from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy, LivelinessPolicy
# Additional Libraries

from enum import Enum
import numpy as np
import cv2
import urllib
from dataclasses import dataclass
import time
from PIL import Image as img
from tensorflow.lite.python.interpreter import Interpreter


# ------------------------ From utils_cgi ------------------------
class ModelType(Enum):
    eth3d = 0
    middlebury = 1
    flyingthings = 2


@dataclass
class CameraConfig:
    baseline: float
    f: float


def load_img(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    return cv2.imdecode(arr, -1)  # 'Load it as it is'


def draw_disparity(disparity_map):
    disparity_map = disparity_map.astype(np.uint8)
    norm_disparity_map = (
                255 * ((disparity_map - np.min(disparity_map)) / (np.max(disparity_map) - np.min(disparity_map))))
    return cv2.applyColorMap(cv2.convertScaleAbs(norm_disparity_map, 1), cv2.COLORMAP_JET)


def draw_depth(depth_map, max_dist, custom_range=None, global_min=None, global_max=None):
    if custom_range:
        min_val, max_val = custom_range
    else:
        min_val, max_val = 0, max_dist

    if global_min is not None and global_max is not None:
        min_val = global_min
        max_val = global_max

    norm_depth_map = 255 * (1 - (depth_map - min_val) / (max_val - min_val))
    norm_depth_map[norm_depth_map < 0] = 0
    norm_depth_map[depth_map == 0] = 0

    return cv2.applyColorMap(cv2.convertScaleAbs(norm_depth_map, 1), cv2.COLORMAP_JET)


# ------------------------ From cgi_stereo -----------------------
drivingStereo_config = CameraConfig(0.546, 1000)


class CGIStereo():

    def __init__(self, model_path, camera_config=drivingStereo_config):
        self.fps = 0
        self.timeLastPrediction = time.time()
        self.frameCounter = 0
        self.camera_config = camera_config

        # Initialize model
        self.model = self.initialize_model(model_path)

    def __call__(self, left_img, right_img):
        return self.estimate_disparity(left_img, right_img)

    def initialize_model(self, model_path):
        # self.interpreter = Interpreter(model_path=model_path, experimental_delegates=[tflite.load_delegate('/usr/lib/x86_64-linux-gnu/libedgetpu.so.1')])

        self.interpreter = Interpreter(model_path=model_path, num_threads=4)
        self.interpreter.allocate_tensors()

        # Get model info
        self.getModel_input_details()
        self.getModel_output_details()

    def estimate_disparity(self, left_img, right_img):
        input_tensor = self.prepare_input(left_img, right_img)

        # Perform inference on the image
        left_disparity = self.inference(input_tensor)
        self.disparity_map = left_disparity

        return self.disparity_map

    def get_depth(self):
        return self.camera_config.f * self.camera_config.baseline / self.disparity_map

    def prepare_input(self, left_img, right_img):
        # Resize images
        w, h, _ = left_img.shape
        wi, hi = (w // 32 + 1) * 32, (h // 32 + 1) * 32

        left_img = cv2.resize(left_img, (wi, hi))
        right_img = cv2.resize(right_img, (wi, hi))
        left_img = cv2.resize(left_img, (self.input_width, self.input_height)).astype(np.float32) / 255
        right_img = cv2.resize(right_img, (self.input_width, self.input_height)).astype(np.float32) / 255
        # Ensure the images are in grayscale if model expects 2 channels
        # Normalize images
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        left_img = (left_img - mean) / std
        right_img = (right_img - mean) / std
        if self.channels == 2:
            left_img = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
            right_img = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
        # Stack and add batch dimension
        # stacked_img = np.concatenate((left_img, right_img), axis=-1)
        # input_tensor = np.expand_dims(stacked_img, axis=0)
        left_img = np.expand_dims(left_img, axis=0)
        right_img = np.expand_dims(right_img, axis=0)
        return left_img, right_img

    def inference(self, input_tensor):
        print(self.input_details[0]['shape'])
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor[1])
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor[0])
        # self.interpreter.set_tensor(self.input_details[1]['index'], input_tensor[1])
        self.interpreter.invoke()
        left_disparity = self.interpreter.get_tensor(self.output_details[0]['index'])

        return np.squeeze(left_disparity)

    def getModel_input_details(self):
        self.input_details = self.interpreter.get_input_details()
        input_shape = self.input_details[0]['shape']
        self.input_height = input_shape[1]
        self.input_width = input_shape[2]
        self.channels = input_shape[3]

    def getModel_output_details(self):
        self.output_details = self.interpreter.get_output_details()
        output_shape = self.output_details[0]['shape']


# ------------------------ ROS2 Node -----------------------------
class StereoDepthEstimation(Node):
    def __init__(self):
        super().__init__('stereo_depth_estimation')
        self.bridge = CvBridge()

        # Initialize the model
        model_path = "cgi_models/cgi_stereo_sceneflow_256x320_float32.tflite"

        camera_config = CameraConfig(baseline=0.05, f=707)
        self.cgi = CGIStereo(model_path, camera_config)

        # Publishers for the depth map and disparity map

        # Subscribe to the left and right image topics
        self.left_img = None
        self.right_img = None
        self.left_sub = self.create_subscription(CompressedImage, '/olive/camera/eye2/image/compressed',
                                                 self.process_left_image, qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.right_sub = self.create_subscription(CompressedImage, '/olive/camera/eye1/image/compressed',
                                                  self.process_right_image,
                                                  qos_profile=rclpy.qos.qos_profile_sensor_data)

        self.depth_pub = self.create_publisher(Image,'stereo_depth_estimation', qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.disparity_pub = self.create_publisher(Image,'stereo_disparity_estimation', qos_profile=rclpy.qos.qos_profile_sensor_data)

    def process_left_image(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        # Decompress the image using OpenCV
        self.left_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.get_logger().info('Left Image received')
        # self.left_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        self.process_images()

    def process_right_image(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        # Decompress the image using OpenCV
        self.right_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.get_logger().info('Right Image received')
        # self.right_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        self.process_images()

    def process_images(self):
        if self.left_img is not None and self.right_img is not None:
            disparity_map = self.cgi(self.left_img, self.right_img)
            self.get_logger().info('disparity_map shape:{}'.format(disparity_map.shape))
            depth_map = self.cgi.get_depth()
            disparity_img = draw_disparity(disparity_map)
            depth_img = draw_depth(depth_map, max_dist=3)
            disparity_msg = self.bridge.cv2_to_imgmsg(disparity_img, "bgr8")
            # disparity_msg = self.bridge.cv2_to_compressed_imgmsg(disparity_msg)
            depth_msg = self.bridge.cv2_to_imgmsg(depth_img, "bgr8")
            # depth_msg = self.bridge.cv2_to_compressed_imgmsg(depth_msg)
            self.disparity_pub.publish(disparity_msg)
            self.depth_pub.publish(depth_msg)
        # Reset the images
        # self.left_img = None
        # self.right_img = None


def main(args=None):
    rclpy.init()
    node = StereoDepthEstimation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
