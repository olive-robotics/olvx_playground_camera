"""
MIT License

Copyright (c) 2023 Olive Robotics GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import rclpy
import math
import time
import io
import os
import pathlib
import threading
import zlib
import collections
import svgwrite

from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Vector3

from PIL import Image
from PIL import ImageDraw

from pose_engine import PoseEngine
from pose_engine import KeypointType

_NUM_KEYPOINTS = 17

EDGES = (
    (KeypointType.NOSE, KeypointType.LEFT_EYE),
    (KeypointType.NOSE, KeypointType.RIGHT_EYE),
    (KeypointType.LEFT_EAR, KeypointType.LEFT_EYE),
    (KeypointType.RIGHT_EAR, KeypointType.RIGHT_EYE),
    (KeypointType.LEFT_EYE, KeypointType.RIGHT_EYE),
    (KeypointType.LEFT_SHOULDER, KeypointType.RIGHT_SHOULDER),
    (KeypointType.LEFT_SHOULDER, KeypointType.LEFT_ELBOW),
    (KeypointType.LEFT_SHOULDER, KeypointType.LEFT_HIP),
    (KeypointType.RIGHT_SHOULDER, KeypointType.RIGHT_ELBOW),
    (KeypointType.RIGHT_SHOULDER, KeypointType.RIGHT_HIP),
    (KeypointType.LEFT_ELBOW, KeypointType.LEFT_WRIST),
    (KeypointType.RIGHT_ELBOW, KeypointType.RIGHT_WRIST),
    (KeypointType.LEFT_HIP, KeypointType.RIGHT_HIP),
    (KeypointType.LEFT_HIP, KeypointType.LEFT_KNEE),
    (KeypointType.RIGHT_HIP, KeypointType.RIGHT_KNEE),
    (KeypointType.LEFT_KNEE, KeypointType.LEFT_ANKLE),
    (KeypointType.RIGHT_KNEE, KeypointType.RIGHT_ANKLE),
)

class AppNode(Node):

    def __init__(self):
        super().__init__('app_node_skeleton')
    
        print('Olive TPU Skeleton Detection v0.2')
        
        self.sub = self.create_subscription(CompressedImage,'/olive/camera/id01/image/compressed',self.image_callback,qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.pub = self.create_publisher(CompressedImage, '/olive/camera/id01/tpu/compressed', 1)
        
        script_dir = pathlib.Path(__file__).parent.absolute()
        self.engine = PoseEngine('models/posenet_mobilenet_v1_075_353_481_quant_decoder_edgetpu.tflite')
        
        # Global variable
        self.busy = False
        self.n = 0
        self.sum_process_time = 0
        self.sum_inference_time = 0

        print('Upload done')
        
    def image_callback(self,msg):
        if not self.busy:
            self.busy = True
            print("Received image data!")
            buffer = io.BytesIO(bytes(msg.data))
            # Open the image buffer using PIL Image
            pil_image = Image.open(buffer)
            pil_image = pil_image.rotate(90)
           
            poses, inference_time = self.engine.DetectPosesInImage(pil_image)
            print('Inference time: %.f ms' % (inference_time * 1000))
           
            print('-------RESULTS--------')
            
            pil_image = pil_image.convert('RGB')
            draw = ImageDraw.Draw(pil_image)
            
            width, height = pil_image.size
            
            
            for pose in poses:
                if pose.score < 0.4: continue
                print('\nPose Score: ', pose.score)
                xys = {}
                
                for label, keypoint in pose.keypoints.items():
                    #print('  %-20s x=%-4d y=%-4d score=%.1f' %#(label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
                    if keypoint.score > 0.4: 
                        xys[label] = (keypoint.point[0] / 1.47, keypoint.point[1] / 1.5)
                        draw.ellipse(
                        xy=[
                            keypoint.point[0] / 1.47 - 2, keypoint.point[1] / 1.5  - 2,
                            keypoint.point[0] / 1.47 + 2, keypoint.point[1] / 1.5  + 2
                        ],
                        fill=(0, 0, 255))
            
                for a, b in EDGES:
                    if a not in xys or b not in xys: continue
                    ax, ay = xys[a]
                    bx, by = xys[b]
                    draw.line(xy=[ax, ay,bx, by],fill=(255, 255, 0),width=3)
           
            print('-------Output--------')
            
            # Save the PIL image as a JPEG in memory
            jpeg_bytes = io.BytesIO()
            pil_image.save(jpeg_bytes, format='JPEG')
            jpeg_data = jpeg_bytes.getvalue()

            # Create a ROS2 CompressedImage message and publish it
            msg = CompressedImage()
            msg.format = 'jpeg'
            msg.data = jpeg_data
            self.pub.publish(msg)
            self.busy = False
        
def main(args=None):
    rclpy.init(args=args)
    app_node = AppNode()
    rclpy.spin(app_node)

    app_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
