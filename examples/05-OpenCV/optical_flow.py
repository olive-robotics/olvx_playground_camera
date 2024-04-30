import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np

class OpticalFlowNode(Node):
    def __init__(self):
        super().__init__('optical_flow_node')
        self.sub = self.create_subscription(
            CompressedImage, '/olive/camera/id01/image/compressed',
            self.image_callback, rclpy.qos.qos_profile_sensor_data
        )
        self.pub = self.create_publisher(
            CompressedImage, '/olive/camera/id01/image/optical_flow/compressed', 10
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

            # Visualize optical flow
            h, w = flow.shape[:2]
            flow_img = np.zeros((h, w, 3), dtype=np.uint8)
            for y in range(0, h, 10):
                for x in range(0, w, 10):
                    fx, fy = flow[y, x]
                    cv2.line(flow_img, (x, y), (int(x + fx), int(y + fy)), (0, 255, 0), 1)
                    cv2.circle(flow_img, (x, y), 2, (0, 0, 255), -1)

            # Convert the OpenCV image to a ROS image message
            _, buffer = cv2.imencode('.jpg', flow_img)
            flow_msg = CompressedImage()
            flow_msg.header = msg.header  # Preserve the header info
            flow_msg.format = "jpeg"
            flow_msg.data = buffer.tobytes()

            # Publish the result
            self.pub.publish(flow_msg)

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
