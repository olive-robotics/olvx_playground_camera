import pathlib
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import io
import os

import PIL
from PIL import Image, ImageDraw
import numpy as np

# MediaPipe Face Landmarker imports
import mediapipe as mp
from mediapipe.tasks.python import vision

# CONFIG
INPUT_TOPIC = '/olive/camera/id001/image/compressed'
OUTPUT_TOPIC = '/olive/camera/id007/image/compressed'
FACE_LANDMARK_MODEL_PATH = '../models/face_landmark_detection.task'

PIL.ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageRelay(Node):
    def __init__(self):
        super().__init__('image_relay')
        self.get_logger().info('Image relay node started')

        # Subscribe to the incoming camera image topic
        self.subscription = self.create_subscription(
            CompressedImage,
            INPUT_TOPIC,
            self.on_image,
            qos_profile=rclpy.qos.qos_profile_sensor_data
        )
        self.get_logger().info(f'Subscribed to {INPUT_TOPIC}')

        # Publisher for the processed image
        self.publisher = self.create_publisher(
            CompressedImage,
            OUTPUT_TOPIC,
            rclpy.qos.qos_profile_sensor_data
        )
        self.get_logger().info(f'Publishing to {OUTPUT_TOPIC}')

        # --- Initialize MediaPipe Face Landmarker ---
        BaseOptions = mp.tasks.BaseOptions
        FaceLandmarker = vision.FaceLandmarker
        FaceLandmarkerOptions = vision.FaceLandmarkerOptions
        VisionRunningMode = vision.RunningMode

        script_dir = pathlib.Path(__file__).parent.absolute()
        face_model_path = os.path.join(script_dir, FACE_LANDMARK_MODEL_PATH)

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=face_model_path),
            running_mode=VisionRunningMode.IMAGE,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.face_landmarker = FaceLandmarker.create_from_options(options)
        self.get_logger().info('Face Landmarker initialized')

    def on_image(self, msg: CompressedImage):
        # Copy and process the incoming image
        relay = CompressedImage()
        relay.header = msg.header
        relay.format = msg.format
        relay.data = msg.data

        self.manipulate_image(relay)
        self.publisher.publish(relay)
        self.get_logger().debug('Published one processed frame')

    def manipulate_image(self, msg: CompressedImage):
        # Decode JPEG to PIL image
        buffer = io.BytesIO(bytes(msg.data))
        pil_image = Image.open(buffer).convert('RGB')
        width, height = pil_image.size

        # --- Face Landmark Detection ---
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=np.asarray(pil_image)
        )
        result = self.face_landmarker.detect(mp_image)

        # Draw landmarks on the image
        draw = ImageDraw.Draw(pil_image)
        if result.face_landmarks:
            # Only first face (num_faces=1)
            for lm in result.face_landmarks[0]:
                x_px = int(lm.x * width)
                y_px = int(lm.y * height)
                r = 2
                draw.ellipse((x_px - r, y_px - r, x_px + r, y_px + r), outline='green')

        # Encode back to JPEG
        out_buffer = io.BytesIO()
        pil_image.save(out_buffer, format='JPEG')
        msg.data = out_buffer.getvalue()
        msg.format = 'jpeg'


def main(args=None):
    rclpy.init(args=args)
    node = ImageRelay()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
