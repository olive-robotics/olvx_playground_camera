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
        
        self.sub = self.create_subscription(CompressedImage,'/olive/camera/eye/image/compressed',self.image_callback,qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.pub = self.create_publisher(CompressedImage, '/olive/one/tpu/compressed', 1)
        
        script_dir = pathlib.Path(__file__).parent.absolute()
        model_file = os.path.join(script_dir, 'test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite')
        label_file = os.path.join(script_dir, 'test_data/coco_labels.txt')
        
        # Global variable
        self.busy = False
        
        print('Uploading tensor model')

        self.labels = read_label_file(label_file) 
        self.interpreter = make_interpreter(model_file)
        self.interpreter.allocate_tensors()
        
        print('Upload done')
        
    def simple_test():
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
            objs = detect.get_objects(self.interpreter, 0.4, scale)
            print('%.2f ms' % (inference_time * 1000))

            print('-------RESULTS--------')
            
            if not objs:
                print('No objects detected')

            for obj in objs:
                print(self.labels.get(obj.id, obj.id))
                print('  id:    ', obj.id)
                print('  score: ', obj.score)
                print('  bbox:  ', obj.bbox)
    
            pil_image = pil_image.convert('RGB')
            draw = ImageDraw.Draw(pil_image)
            
            for obj in objs:
                bbox = obj.bbox
                draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],outline='red')
                draw.text((bbox.xmin + 10, bbox.ymin + 10),'%s\n%.2f' % (self.labels.get(obj.id, obj.id), obj.score),fill='red')   
            
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
