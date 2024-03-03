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
    
        print('Olive TPU Hello World v0.1')
        
        # Specify the TensorFlow model, labels, and image
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, 'test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite')
        label_file = os.path.join(script_dir, 'test_data/inat_bird_labels.txt')
        image_file = os.path.join(script_dir, 'test_data/parrot.jpg')

        print('step1')
        
        # Initialize the TF interpreter
        interpreter = edgetpu.make_interpreter(model_file)
        interpreter.allocate_tensors()

        print('step2')
        
        # Resize the image
        size = common.input_size(interpreter)
        image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)

        print('step3')
        # Run an inference
        common.set_input(interpreter, image)
        interpreter.invoke()
        classes = classify.get_classes(interpreter, top_k=1)

        print('step4')
        # Print the result
        labels = dataset.read_label_file(label_file)
        for c in classes:
          print('%s: %.5f' % (labels.get(c.id, c.id), c.score))
        
       
def main(args=None):
    rclpy.init(args=args)
    app_node = AppNode()
    rclpy.spin(app_node)

    app_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

