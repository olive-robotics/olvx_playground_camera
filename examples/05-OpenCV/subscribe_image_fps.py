import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
import time

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            CompressedImage,
            '/olive/camera/id01/image/compressed',
            self.listener_callback,
            rclpy.qos.qos_profile_sensor_data,
            )
        self.subscription  # prevent unused variable warning
        self.last_time = time.time()
        self.frame_count = 0

    def listener_callback(self, msg):
        # Calculate frame rate
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 1.0:  # every second
            frame_rate = self.frame_count / (current_time - self.last_time)
            self.frame_count = 0
            self.last_time = current_time
            self.get_logger().info('Frame Rate: {:.2f} FPS'.format(frame_rate))

        # Convert compressed image message to OpenCV image
        np_arr = np.frombuffer(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Display image
        cv2.imshow('camera_image', image_np)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

