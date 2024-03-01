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

class AppNode(Node):

    def __init__(self):
        super().__init__('app_node')
    
        print('Olive TPU Object Detection v0.2')
        
        self.sub = self.create_subscription(CompressedImage,'/olive/camera/id01/ai/image/compressed',self.image_callback,qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.pub = self.create_publisher(String, '/olive/tpu', 1)
        
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, 'models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite')
        label_file = os.path.join(script_dir, 'models/coco_labels.txt')
        
        # Global variable
        self.busy = False
        
        print('Uploading tensor model')

        self.labels = read_label_file(label_file) 
        self.interpreter = make_interpreter(model_file)
        self.interpreter.allocate_tensors()
        self.first_time = 0
        self.msg = String()
        self.scale = (1,1)
        
        print('Upload done')
        
    def image_callback(self,msg):
        callback_start = time.monotonic()
        if not self.busy:
            self.busy = True
            
            start = time.perf_counter()
                
            buffer = io.BytesIO(bytes(msg.data))
            pil_image = Image.open(buffer)

            common.set_input(self.interpreter, pil_image)
            
            self.interpreter.invoke()
            
            objs = detect.get_objects(self.interpreter, 0.4,self.scale )

            objs_str = ";".join([f"{obj.id},{obj.score},{obj.bbox.xmin},{obj.bbox.ymin},{obj.bbox.xmax},{obj.bbox.ymax}" for obj in objs])
            
            self.msg.data = objs_str
            self.pub.publish(self.msg)
            
            inference_time = time.perf_counter() - start
            print('%.2f ms (ALL)' % (inference_time * 1000))
               
            self.busy = False
       
def main(args=None):
    rclpy.init(args=args)
    app_node = AppNode()
    rclpy.spin(app_node)

    app_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

