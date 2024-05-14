import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import yaml

class ImageRectifier(Node):
    def __init__(self):
        super().__init__('image_rectifier')
        self.subscription = self.create_subscription(
            CompressedImage,
            'input/compressed_image',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(CompressedImage, 'output/rectified_compressed_image', 10)
        self.bridge = CvBridge()

        # Load camera calibration data
        with open("ost.yaml", "r") as file:
            self.camera_info = yaml.safe_load(file)

        # Prepare rectification map
        camera_matrix = np.array(self.camera_info['camera_matrix']['data']).reshape((3, 3))
        dist_coeffs = np.array(self.camera_info['distortion_coefficients']['data'])
        self.map1, self.map2 = cv2.initUndistortRectifyMap(
            camera_matrix, dist_coeffs, None, None, (640, 480), cv2.CV_16SC2)

    def listener_callback(self, msg):
        # Convert ROS2 compressed image message to OpenCV format
        cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # Rectify the image
        rectified_image = cv2.remap(cv_image, self.map1, self.map2, cv2.INTER_LINEAR)

        # Convert OpenCV format back to ROS2 compressed image message
        rectified_msg = self.bridge.cv2_to_compressed_imgmsg(rectified_image)

        # Publish the rectified image
        self.publisher.publish(rectified_msg)

def main(args=None):
    rclpy.init(args=args)
    image_rectifier = ImageRectifier()
    rclpy.spin(image_rectifier)
    image_rectifier.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
