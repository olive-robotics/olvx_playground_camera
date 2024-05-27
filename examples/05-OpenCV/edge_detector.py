import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np

class EdgeDetectionNode(Node):
    def __init__(self):
        super().__init__('edge_detection_node')
        self.sub = self.create_subscription(
            CompressedImage, '/olive/camera/id01/image/compressed',
            self.image_callback, rclpy.qos.qos_profile_sensor_data
        )
        self.pub = self.create_publisher(
            CompressedImage, '/olive/camera/id01/image/edges/compressed', 10
        )
        print("ready")

    def image_callback(self, msg):
        # Convert the ROS image message to an OpenCV image
        print("repub1")
        
        np_arr = np.frombuffer(msg.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Perform edge detection
        edges = cv2.Canny(cv_image, 100, 200)
        
        # Convert the OpenCV image to a ROS image message
        _, buffer = cv2.imencode('.jpg', edges)
        edges_msg = CompressedImage()
        edges_msg.header = msg.header  # Preserve the header info
        edges_msg.format = "jpeg"
        edges_msg.data = buffer.tobytes()
        
        # Publish the result
        self.pub.publish(edges_msg)
        
        print("repub2")

def main():
    rclpy.init()
    node = EdgeDetectionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
