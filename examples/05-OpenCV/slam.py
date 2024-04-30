import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
import cv2
import numpy as np

class SimpleSLAMNode(Node):
    def __init__(self):
        super().__init__('simple_slam_node')
        self.sub = self.create_subscription(
            CompressedImage, '/olive/camera/cam01/image/compressed',
            self.image_callback, rclpy.qos.qos_profile_sensor_data
        )
        self.pose_pub = self.create_publisher(
            PoseStamped, '/olive/camera/cam01/pose', 10
        )
        self.map_pub = self.create_publisher(
            OccupancyGrid, '/olive/camera/cam01/map', 10
        )
        self.prev_image = None
        self.orb = cv2.ORB_create()
        self.map = np.zeros((200, 200), dtype=np.int8)

    def image_callback(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

        if self.prev_image is not None:
            # Step 1: Feature Detection and Matching
            kp1, des1 = self.orb.detectAndCompute(self.prev_image, None)
            kp2, des2 = self.orb.detectAndCompute(image, None)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)

            # Step 2: Motion Estimation (simplified, assumes planar motion)
            src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            # Step 3: Map Update (simplified, assumes 2D motion)
            self.map[int(M[1, 2]) + 100, int(M[0, 2]) + 100] = 100  # Marking observed area

            # Step 4: Publishing Data (simplified, assumes 2D motion)
            pose_msg = PoseStamped()
            pose_msg.header.stamp = msg.header.stamp
            pose_msg.header.frame_id = msg.header.frame_id
            pose_msg.pose.position.x = float(M[0, 2])  # Translation in x
            pose_msg.pose.position.y = float(M[1, 2])  # Translation in y
            self.pose_pub.publish(pose_msg)

            map_msg = OccupancyGrid()
            map_msg.header.stamp = msg.header.stamp
            map_msg.header.frame_id = msg.header.frame_id
            map_msg.info.resolution = 1.0
            map_msg.info.width = 200
            map_msg.info.height = 200
            map_msg.data = self.map.flatten().tolist()
            self.map_pub.publish(map_msg)

        self.prev_image = image

def main():
    rclpy.init()
    node = SimpleSLAMNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

