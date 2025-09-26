import cv2
import tensorflow as tf
import tflite_runtime.interpreter as tflite
import time
import urllib.request
import argparse
import rclpy
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy, LivelinessPolicy
from rclpy.duration import Duration
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

class MonoDepthEstimator(Node):
    """
    A ROS2 Node that listens for a compressed image, uses MiDaS21 model for depth map estimation, and publishes these depth maps.
    The node subscribes to the topic /olive/one/camera/compressed that publishes CompressedImage messages.
    It uses a TFlite model to estimate depth maps from the images and publishes the depth maps as Image messages on the topic /depth_map.
    Attributes:
        subscription (Subscription): Subscriber object for image data
        publisher (Publisher): Publisher object for depth maps
        interpreter (Interpreter): TFLite model interpreter
        input_details (list): Details of the TFLite model input tensor
        output_details (list): Details of the TFLite model output tensor
        bridge (CvBridge): Bridge between OpenCV and ROS image formats
    """
    def __init__(self, execution_mode):
        """
        Initializes the MonoDepthEstimator Node
        The method creates a subscription to images data and a publisher for depth maps.
        It downloads and loads the MiDaS21 model v2_1 for depth estimation and sets up a CvBridge for image format conversion.
        rclpy.qos.qos_profile_sensor_data
        /olive/one/camera/compressed
        """
        super().__init__('camera_subscriber')
        qos_profile = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            liveliness=LivelinessPolicy.AUTOMATIC,
)
        self.subscription = self.create_subscription(
            CompressedImage,
            '/olive/camera/id01/image/compressed',
            self.listener_callback,
            qos_profile=rclpy.qos.qos_profile_sensor_data,
        )
        self.subscription  # prevent unused variable warning
        self.publisher = self.create_publisher(Image, 'depth_map', 2)

        # Download the TFLite model
        url, filename = ("https://github.com/intel-isl/MiDaS/releases/download/v2_1/model_opt.tflite", "model_opt.tflite")
        urllib.request.urlretrieve(url, filename)

        # Load the TFLite model
        self.load_model(execution_mode)
        #self.interpreter = tf.lite.Interpreter(model_path="model_opt.tflite")

        #Load the TFLite model with Pycoral
        #self.interpreter = tflite.Interpreter(model_path="model_opt.tflite",
        #                         experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        #self.interpreter = edgetpu.make_interpreter("model_opt.tflite")

        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Setup CvBridge
        self.bridge = CvBridge()
        # Initiate execution mode

    def load_model(self, execution_mode):
        """
        Load the TensorFlow Lite model using different execution modes.

        This method allows you to select between different execution modes: CPU, GPU, and TPU.
        It uses the TensorFlow Lite Interpreter to load the model with a delegate appropriate for the specified mode.

        Args:
        execution_mode (str): The execution mode to use. Options are 'GPU', 'TPU', or 'CPU'.
        """
        model_path="model_opt.tflite"
        if execution_mode == 'GPU':
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                try:
                    # Specify a particular GPU to use
                    tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
                    # load the model for GPU execution
                    self.interpreter = tf.lite.Interpreter(model_path=model_path)
                except RuntimeError as e:
                    print(e)


        elif execution_mode == 'TPU':
            # load the model for TPU execution
            #self.interpreter = tf.lite.Interpreter(model_path=model_path,
            #                     experimental_delegates=[tflite.load_delegate('/usr/lib/x86_64-linux-gnu/libedgetpu.so.1')])
            print("")
        else:
            # default to CPU execution
            with tf.device('/CPU:0'):
                self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

    def listener_callback(self, msg):
        """
        Callback function for the subscription to image data.

        The function converts the image data to a numpy array, decompresses the image using OpenCV, and pre-processes it for the TFLite model.
        It runs inference on the pre-processed image using the TFLite MiDaS21 model, post-processes the output to create a depth map, and publishes the depth map as a color jet map.

        Args:
            msg (CompressedImage): The image data message received from the subscription
        """
        # Convert the compressed image data to a numpy array
        np_arr = np.frombuffer(msg.data, np.uint8)
        # Decompress the image using OpenCV
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # Convert the image to RGB format
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) / 255.0
        # Resize the image to 256x256 pixels
        img_resized = tf.image.resize(img_rgb, [256,256], method='bicubic', preserve_aspect_ratio=False)
        # Normalize the pixel values
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        img_input = (img_resized.numpy() - mean) / std
        reshape_img = img_input.reshape(1,256,256,3)
        tensor = tf.convert_to_tensor(reshape_img, dtype=tf.float32)

        # Run inference on the input tensor using the MiDaS21 model
        self.interpreter.set_tensor(self.input_details[0]['index'], tensor)
        self.interpreter.invoke()
        start_time = time.time()
        self.interpreter.invoke()
        end_time = time.time()
        inference_time = end_time - start_time
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        self.get_logger().info(f"Inference time: {inference_time} seconds")
        prediction = output.reshape(256, 256)
        # Resize the depth map to the original image size
        prediction = cv2.resize(prediction, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
        depth_min = prediction.min()
        depth_max = prediction.max()
        depth_map = (255 * (prediction - depth_min) / (depth_max - depth_min)).astype("uint8")
        depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)
        # Publish the output depth map as a ROS2 message
        depth_map_msg = self.bridge.cv2_to_imgmsg(depth_map, encoding='bgr8')
        depth_map_msg.header.stamp = msg.header.stamp
        self.publisher.publish(depth_map_msg)
        #self.publisher.publish(msg)
        #self.get_logger().info('Received image timestamp: {}'.format(msg.header.stamp))

def main(args=None):
    """
    Main entry point for the ROS2 Node MonoDepthEstimator.

    It initializes the ROS2 Python library, creates an instance of the MonoDepthEstimator, spins the node to keep it from exiting, and then cleans up by destroying the node and shutting down the library.

    Args:
        args: Command-line arguments
    """
    rclpy.init(args=args)
    parser = argparse.ArgumentParser(description='MonoDepthEstimator Node')
    parser.add_argument('--execution', type=str, default='CPU',
                        help='Execution mode: "CPU", "GPU", or "TPU"')
    args, _ = parser.parse_known_args()
    mono_depth_estimator = MonoDepthEstimator(execution_mode=args.execution)
    rclpy.spin(mono_depth_estimator)
    mono_depth_estimator.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
