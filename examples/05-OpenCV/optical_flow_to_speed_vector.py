import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
import cv2
import numpy as np

class OpticalFlowNode(Node):
    def __init__(self):
        super().__init__('optical_flow_node')
        self.sub = self.create_subscription(
            CompressedImage, '/olive/camera/cam01/image/compressed',
            self.image_callback, rclpy.qos.qos_profile_sensor_data
        )
        self.pub = self.create_publisher(
            Twist, '/olive/camera/cam01/optical_flow/velocity', 10
        )
        self.prev_gray = None

    def image_callback(self, msg):
        # Convert the ROS image message to an OpenCV image
        np_arr = np.frombuffer(msg.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is not None:
            # Compute optical flow
            flow = cv2.calcOpticalFlowFarneback(self.prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            # Calculate the overall motion
            avg_flow = np.mean(flow, axis=(0, 1))

            # Create and publish a Twist message representing the overall motion
            twist_msg = Twist()
            twist_msg.linear.x = float(avg_flow[0])
            twist_msg.linear.y = float(avg_flow[1])
            self.pub.publish(twist_msg)

        self.prev_gray = gray

def main():
    rclpy.init()
    node = OpticalFlowNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
