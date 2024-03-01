import rclpy
import math
import time
import io
import os
import pathlib
import threading
import zlib

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

_NUM_KEYPOINTS = 17

class AppNode(Node):

    def __init__(self):
        super().__init__('app_node_skeleton')
    
        print('Olive TPU Skeleton Detection v0.1')
        
        self.sub = self.create_subscription(CompressedImage,'/olive/camera/eye/image/compressed',self.image_callback,qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.pub = self.create_publisher(CompressedImage, '/olive/camera/eye/tpu/compressed', 1)
        
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, 'test_data/movenet_single_pose_lightning_ptq_edgetpu.tflite')
        
        # Global variable
        self.busy = False
        
        print('Uploading tensor model')

        self.interpreter = make_interpreter(model_file)
        self.interpreter.allocate_tensors()
        
        print('Upload done')
        
    def image_callback(self,msg):
        if not self.busy:
            self.busy = True
            print("Received image data!")
            buffer = io.BytesIO(bytes(msg.data))
            # Open the image buffer using PIL Image
            pil_image = Image.open(buffer)
            _, scale = common.set_resized_input(
            self.interpreter, pil_image.size, lambda size: pil_image.resize(size, Image.ANTIALIAS))
            print("Received image data and converted to PIL!")
            
            print('----INFERENCE TIME----')
            
            start = time.perf_counter()
            self.interpreter.invoke()
            inference_time = time.perf_counter() - start
            
            pose = common.output_tensor(self.interpreter, 0).copy().reshape(_NUM_KEYPOINTS, 3)
            print(pose)
            
            print('%.2f ms' % (inference_time * 1000))

            print('-------RESULTS--------')
            
            pil_image = pil_image.convert('RGB')
            draw = ImageDraw.Draw(pil_image)
            
            width, height = pil_image.size
            for i in range(0, _NUM_KEYPOINTS):
                draw.ellipse(
                    xy=[
                        pose[i][1] * width - 2, pose[i][0] * height - 2,
                        pose[i][1] * width + 2, pose[i][0] * height + 2
                    ],
                    fill=(255, 0, 0))
            
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
