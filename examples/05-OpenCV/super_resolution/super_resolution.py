import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np

class SuperResolutionNode(Node):
    def __init__(self):
        super().__init__('super_resolution_node')
        self.sub = self.create_subscription(
            CompressedImage, '/olive/camera/cam01/image/compressed',
            self.image_callback, rclpy.qos.qos_profile_sensor_data
        )
        self.pub = self.create_publisher(
            CompressedImage, '/olive/camera/cam01/image_super_res/compressed', 10
        )
        self.bridge = CvBridge()
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        # Assuming you have a pre-trained model (e.g., "EDSR_x4.pb")
        # This is just a placeholder, you'll need to replace with an actual model file
        self.sr.readModel('EDSR_x2.pb')
        self.sr.setModel("edsr", 2)  # Assuming a scaling factor of 4

    def image_callback(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        result = self.sr.upsample(image)
        result_msg = self.bridge.cv2_to_compressed_imgmsg(result)
        result_msg.header = msg.header  # Preserve the header info
        self.pub.publish(result_msg)

def main():
    rclpy.init()
    node = SuperResolutionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

