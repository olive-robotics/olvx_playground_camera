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

import pandas as pd

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

from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from joblib import dump, load

import numpy as np
import time
import tflite_runtime.interpreter as tflite
from threading import Thread
#import rospy
#from std_msgs.msg import String
from collections import deque
#rospy.init_node('recognition', anonymous=True)

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
    
        print('Olive TPU Gesture Recognition MLP v0.3')
        
        self.mlp = load('mlp_model.joblib')
        self.le = load('label_encoder.joblib')
        
        self.sub = self.create_subscription(CompressedImage,'/olive/camera/owl1eye/image/compressed',self.image_callbackTest,qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.pub = self.create_publisher(CompressedImage, '/olive/camera/owl1eye/tpu/compressed', 1)
        self.pub_result = self.create_publisher(String, '/olive/camera/owl1eye/tpu/gesture', 1)
        
        script_dir = pathlib.Path(__file__).parent.absolute()
        #self.engine = PoseEngine('test_data/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
        self.engine = PoseEngine('test_data/posenet_mobilenet_v1_075_353_481_quant_decoder_edgetpu.tflite')
        
        # Global variable
        self.busy = False
        self.n = 0
        self.sum_process_time = 0
        self.sum_inference_time = 0
        self.gesture_result = "none"
        #self.trainMLP()
        print('Upload done')
        
    def trainMLP(self):
        print('MLP Training')
        # Define column names for your data
        columns = [f'{i}{j}' for i in 'XY' for j in range(1, 18)] + ['Label']
        
        # Read the data from the text file
        df = pd.read_csv('data.txt', header=None, names=columns)
        
        # We need to convert the labels into numerical form for MLP
        le = LabelEncoder()
        df['Label'] = le.fit_transform(df['Label'])

        # Split the data into features and labels
        X = df.drop('Label', axis=1)
        y = df['Label']

        # Split the data into a training set and a testing set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Define the MLP
        mlp = MLPClassifier(hidden_layer_sizes=(50,), max_iter=1000)
        
        # Train the MLP
        mlp.fit(X_train, y_train)

        # Predict the labels of the test set
        y_pred = mlp.predict(X_test)

        # Print the accuracy of the model
        print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
        
        # Save the model and the label encoder
        dump(mlp, 'mlp_model.joblib')
        dump(le, 'label_encoder.joblib')
        
    def image_callbackTest(self,msg):
        if not self.busy:
            self.busy = True
            #print("Received image data!")
            buffer = io.BytesIO(bytes(msg.data))
            # Open the image buffer using PIL Image
            pil_image = Image.open(buffer)
            pil_image = pil_image.rotate(90)
           
            poses, inference_time = self.engine.DetectPosesInImage(pil_image)
            #print('Inference time: %.f ms' % (inference_time * 1000))
        
            pil_image = pil_image.convert('RGB')
            draw = ImageDraw.Draw(pil_image)
            
            width, height = pil_image.size
            
            self.xys = {}
    
            for pose in poses:
                if pose.score < 0.4: continue

                for label, keypoint in pose.keypoints.items():
                    #print('  %-20s x=%-4d y=%-4d score=%.1f' %#(label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
                    if keypoint.score > 0.4: 
                        self.xys[label] = (keypoint.point[0] / 1.47, keypoint.point[1] / 1.5)
                        draw.ellipse(
                        xy=[
                            keypoint.point[0] / 1.47 - 2, keypoint.point[1] / 1.5  - 2,
                            keypoint.point[0] / 1.47 + 2, keypoint.point[1] / 1.5  + 2
                        ],
                        fill=(0, 0, 255))

                for a, b in EDGES:
                    if a not in self.xys or b not in self.xys: continue
                    ax, ay = self.xys[a]
                    bx, by = self.xys[b]
                    draw.line(xy=[ax, ay,bx, by],fill=(255, 255, 0),width=3)

                #print(len(self.xys))

                if len(self.xys) == 17:
                    # Collect all x, y values into a list
                    values = []
                    for label, (x, y) in self.xys.items():
                        values.append(str(x))
                        values.append(str(y))

                    # Append the label at the end
                    #values.append('4')

                    # Create a single string of all values separated by comma
                    line = ','.join(values)
                    
                    # Split the string by comma and convert each element to a float
                    new_data = [[float(coord) for coord in line.split(',')]]
                   
                    # Use the trained model to predict the label of the new data
                    new_pred = self.mlp.predict(new_data)

                    # The output is in numerical form, so we convert it back into string form
                    new_pred_label = self.le.inverse_transform(new_pred)
                    self.gesture_result = str(new_pred_label[0])

                    print(f"The predicted gesture is: {new_pred_label[0]}")
                
            # Save the PIL image as a JPEG in memory
            jpeg_bytes = io.BytesIO()
            pil_image.save(jpeg_bytes, format='JPEG')
            jpeg_data = jpeg_bytes.getvalue()

            # Create a ROS2 CompressedImage message and publish it
            msg = CompressedImage()
            msg.format = 'jpeg'
            msg.data = jpeg_data
            self.pub.publish(msg)
           
            # Create a ROS2 CompressedImage message and publish it
            msg_text = String()
            msg_text.data = self.gesture_result
            self.pub_result.publish(msg_text)
            
            self.busy = False
            
    def image_callback(self,msg):
        if not self.busy:
            self.busy = True
            #print("Received image data!")
            buffer = io.BytesIO(bytes(msg.data))
            # Open the image buffer using PIL Image
            pil_image = Image.open(buffer)
            pil_image = pil_image.rotate(90)
           
            poses, inference_time = self.engine.DetectPosesInImage(pil_image)
            #print('Inference time: %.f ms' % (inference_time * 1000))
        
            pil_image = pil_image.convert('RGB')
            draw = ImageDraw.Draw(pil_image)
            
            width, height = pil_image.size
            
            self.xys = {}
    
            for pose in poses:
                if pose.score < 0.4: continue

                for label, keypoint in pose.keypoints.items():
                    #print('  %-20s x=%-4d y=%-4d score=%.1f' %#(label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
                    if keypoint.score > 0.4: 
                        self.xys[label] = (keypoint.point[0] / 1.47, keypoint.point[1] / 1.5)
                        draw.ellipse(
                        xy=[
                            keypoint.point[0] / 1.47 - 2, keypoint.point[1] / 1.5  - 2,
                            keypoint.point[0] / 1.47 + 2, keypoint.point[1] / 1.5  + 2
                        ],
                        fill=(0, 0, 255))

                for a, b in EDGES:
                    if a not in self.xys or b not in self.xys: continue
                    ax, ay = self.xys[a]
                    bx, by = self.xys[b]
                    draw.line(xy=[ax, ay,bx, by],fill=(255, 255, 0),width=3)

                #print(len(self.xys))

                if len(self.xys) == 17:
                    # Collect all x, y values into a list
                    values = []
                    for label, (x, y) in self.xys.items():
                        values.append(str(x))
                        values.append(str(y))

                    # Append the label at the end
                    values.append('4')

                    # Create a single string of all values separated by comma
                    line = ','.join(values)
                    
                    with open('data2.txt', 'a') as f:
                        # Write the headers
                        # Write this line to the file
                        f.write(line + '\n')
                    
                    print("Saved")
                
            # Save the PIL image as a JPEG in memory
            jpeg_bytes = io.BytesIO()
            pil_image.save(jpeg_bytes, format='JPEG')
            jpeg_data = jpeg_bytes.getvalue()

            # Create a ROS2 CompressedImage message and publish it
            msg = CompressedImage()
            msg.format = 'jpeg'
            msg.data = jpeg_data
            self.pub.publish(msg)
           
            # Create a ROS2 CompressedImage message and publish it
            msg_text = String()
            msg_text.data = self.gesture_result
            self.pub_result.publish(msg_text)
            
            self.busy = False
            
def main(args=None):
    rclpy.init(args=args)
    app_node = AppNode()
    rclpy.spin(app_node)

    app_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
