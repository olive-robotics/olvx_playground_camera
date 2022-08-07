#!/usr/bin/env python3
import rclpy
import numpy as np
import math
import time
import io
import os
import pathlib
import threading
import zlib
import collections
import time
import tflite_runtime.interpreter as tflite
from threading import Thread

from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Vector3

from PIL import Image
from PIL import ImageDraw

#import rospy
#from std_msgs.msg import String
from collections import deque
#rospy.init_node('recognition', anonymous=True)

_NUM_KEYPOINTS = 17

######Parameters to configure#########################
FILEPATH_POSE_MODEL_TPU='test_data/pose_model_thunder_uint8_tpu_edgetpu.tflite'
FILEPATH_CLASSIFICATION_MODEL_TPU='test_data/pose_classifier_edgetpu.tflite'
FILEPATH_CLASSIFICATION_MODEL_CPU='test_data/pose_classifier.tflite'
#####################

class Inference(Node):
    def __init__(self):
        super().__init__('app_node_gesture_recognition_tpu')
        
        print('Olive TPU Gesture Recognition TPU v0.1')
        
        self.sub = self.create_subscription(CompressedImage,'/olive/camera/owl1eye/image/compressed',self.image_callback,qos_profile=rclpy.qos.qos_profile_sensor_data)
        self.pub = self.create_publisher(CompressedImage, '/olive/camera/owl1eye/tpu/compressed', 1)
        self.pub_result = self.create_publisher(String, '/olive/camera/owl1eye/tpu/gesture', 1)
        
        self.next_previous={'nose':[0,0],'left_eye':[0,0],'right_eye':[0,0],'left_ear':[0,0],'right_ear':[0,0],'left_shoulder':[0,0],'right_shoulder':[0,0],'left_ellbow':[0,0],'right_ellbow':[0,0],'left_wrist':[0,0],'right_wrist':[0,0],'left_hip':[0,0],'right_hip':[0,0],'left_knee':[0,0],'right_knee':[0,0],'left_ankle':[0,0],'right_ankle':[0,0]}# initialize neutral detection result, need for first comparison at filter
        
        #####Initialize classes for Inference and ROS Communication#############
        self.joint_model_class=run_pose_joint_model()#Key point extraction model
        self.classification_class=run_classification_model()#Classification model
        
        #####Configuration of PiCamera object, lower latency than open cv video capture
        self.new_image = False
        self.latest_image=[]
        ##Thread(target=self.record, args=()).start()##Declare thread for recording image. I/O operations can be threaded to accelerate program
    
    def image_callback(self,msg):
        print("Received image data!")
        buffer = io.BytesIO(bytes(msg.data))
        # Open the image buffer using PIL Image
        pil_image = Image.open(buffer)
        pil_image = pil_image.rotate(90)
        self.latest_image = pil_image.resize((256, 256))
        image = self.latest_image
        # Convert Pillow image to NumPy array
        image = np.array(image)
        # Ensure it's uint8 format
        image = image.astype(np.uint8)
        image=image.reshape((1,256,256,3)) #Add batch diemension, 256*256-> image resolution,3-> colour cannels,-> 1 batch dimension for MoveNet
        result=self.joint_model_class.run_inference(image)#run inference and stores tensor returend py interpreter
        result=np.squeeze(np.array(result),(0,1)).flatten().tolist()#converts result to 1 dimensinoal list. Data extraction is easier in next step
        #MoveNet outputs a tensor containing 51 values, Each detected keypoint has an x and y coordinate as well as a score indicating reliability of prediction
        #-> 17 Keypoints times 3 values = 51 values in total
        #The classification is only based on the koordinates. Hence they have to be extracted
        #They are stored in a dictionary for accessing easily
        next={'nose':result[0:2],'left_eye':result[3:5],'right_eye':result[6:8],'left_ear':result[9:11],'right_ear':result[12:14],'left_shoulder':result[15:17],'right_shoulder':result[18:20],'left_ellbow':result[21:23],'right_ellbow':result[24:26],'left_wrist':result[27:29],'right_wrist':result[30:32],'left_hip':result[33:35],'right_hip':result[36:38],'left_knee':result[39:41],'right_knee':result[42:44],'left_ankle':result[45:47],'right_ankle':result[48:50]}#Extraction of keypoints
        ####################################################
        
        pil_image = pil_image.convert('RGB')
        draw = ImageDraw.Draw(pil_image)
        width, height = pil_image.size
        
        for i in range(0, _NUM_KEYPOINTS - 1):
            j = i * 3
            draw.ellipse(
                xy=[
                    result[j] - 2, result[j + 1] - 2,
                    result[j] + 2, result[j + 1] + 2
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
            
        if self.check_sceleton(next):#If key points passes the filter, the programm will proceed 
            ####Classificaiton prepare and process###############
            num=[2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50] #specifiy indices to delet (accuracy)
            result=np.asarray(np.delete(result,num,axis=0)).astype('float32')#delete Accuracy and convert to float32
            result=self.normalization(result)#apply normalization
            result=np.asarray(result).astype('float32')#assure float32 format
            result=np.expand_dims(result,axis=0)#add batch dimension for classificaiton net
            result=self.classification_class.run_inference(result)#run inference
            #######Get result with highest score#####
            new=[]
            num=0
            #Iterates through results and created a list
            for a in result[0]:
                new.append([a,num])
                num+=1
            result=new
            result.sort(key=lambda x: x[0],reverse=True) #Sorting concerning the prediction score stored at index 0
            ######################################################
            res=str(result[0][1])#get number of gesture with highest prediciton score
            if result[0][0]>0.80: #filters gestures with low prediction score
                #q.appendleft(res) # queue for sequence testing, disabled
                if res != '6' and res !='16' and res!='5' and res!='8' and res!='9' and res!='12' and res!='2' and res!='17' and res!='4' and res!='14' and res!='0' and res!='7' and res!='18' and res!='3':
                    #if q[0]==q[1]==q[2]==q[3]==q[4]: #checks if five last predictions are the same, disabled
                        #self.ros_communication_class.send(res) #sends detection via ROS publisher
                        print(str(result[0][1]))
            else :
                #self.ros_communication_class.send('------')  # in case prediciton score to low, a no prediction is send actively
                pass
        else :
            #self.ros_communication_class.send('------') #in case key points do not pass the filter, a no prediction is send actively
            print("Filter error")
            pass
        
    ###Checks sceleton logic in order to differ between noise and proper sceleton. 
    # Firstly the basic skeleton logic is checked. Nose above shoulder, shoulder above hip etc. 
    # Secondly It is compared how much the keypoints have moved in comparision to the previous picture       
    def check_sceleton(self,next):  
        print(next['nose'][0])
        #y value of keypoint is stored at index 0, in the coordinate system y=0 is at the top and y=1 at the bottom
        #Hence if the nose is over the shoulder the y value of the nose has to be samaller (<) than the one of the shoulder
        #If statement checks basic skeleton logic, Nose above shoulder, shoulder above hip etc. .
        if ((next['nose'][0]<next['left_shoulder'][0]) and (next['nose'][0]<next['right_shoulder'][0])and next['left_shoulder'][0]<next['left_hip'][0]) and (next['right_shoulder'][0]<next['right_hip'][0]) and (next['right_hip'][0]<next['right_knee'][0]) and (next['left_hip'][0]<next['left_knee'][0]) and (next['left_knee'][0]<next['left_ankle'][0] and (next['right_knee'][0]<next['right_ankle'][0])): 
            sum=0 #The absolute squared values of key point differences are accumulated with this variable
            #For loop iterates over each key point in the dictionary of the latest frame and the corresponing keypoint of the previous picture
            #The squared distance is calculated 
            for a in next:
                sum+=((float(next[a][0])-float(self.next_previous[a][0]))**2)+((float(next[a][1])-float(self.next_previous[a][1]))**2)
            sum=sum/17 #Calculate average difference
            if sum<0.0001: #If difference beneath a certain threshold True is returned, filter is passed
                self.next_previous=next #latest picture becomes previous picture for next iteration
                return True
            else:
                self.next_previous=next #latest picture becomes previous picture for next iteration
                return False
        else: #in case the basic skeleton logic is not fulfilled the filter is not passed successfully 
            self.next_previous=next #latest picture becomes previous picture for next iteration
            return False

    ##The key point coordinates are normalized before classifying them
    # The Center of the body is assumed to be between the hips. 
    # Firstly y and x data are seperated
    # Secondly the center points are calculated and the koordinates shifted to the center
    # Thirdly the scale factor is calculated by finding min and max of y values
    # Fourthly the key point koordinates get scaled 
    def normalization(self,data):
    
        # Seperating y and x data
        y_list=data[[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]]
        x_list=data[[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33]]
        #Calculaiton of body center
        y_center=(y_list[11]+y_list[12])/2
        x_center=(x_list[11]+x_list[12])/2
        #Shift key points to the center for finding minimum boundary offsets
        for a in range(len(y_list)):
            y_list[a]+=(0.5-y_center)
            x_list[a]+=(0.5-x_center)
        #Minimum and maximum values are generated, minmum offsets to the pictures boundaries are calculated
        y_list.sort()
        x_list.sort()
        delta_y_min=y_list[0]
        delta_y_max=1-y_list[16]
        #Determine scale factor
        scale_points=(0.5)/(0.5-min(delta_y_min,delta_y_max))
        #Scale keypoints and return result
        result=[]# zero initialization 
        count=1#counting for alternate processing of y and x keypoints
        #Iterates through function input
        #first Iteration count % 2 is equals to 1. This is interpreted as True, Hence y data are processed.
        #second iteration count % 2 is equals to 0. This is interpreted as False, Hence x data are processed.
        #Keypoint get shifted and scaled
        for a in iter(data):
            ##Y koordinates
            if count % 2:
                help=a+(0.5-y_center)#Shift
                delta_y=(help-0.5)*scale_points#Scale
                result.append(0.5+delta_y)#Append

            ##X koordinates
            else: 
                help=a+(0.5-x_center)#Shift
                delta_x=(help-0.5)*scale_points#Scale
                result.append(0.5+delta_x)#Append
            count+=1
        return result
            
#Class for joint detection model
#With enabling/disabling the first two lines (self.interpreter) it can be selected whether the model should run on CPU or TPU
#For the TPU Models a delegate has to be given as an input parameter for the interpreter. The delegate is required by the interpreter
#to deal with the specific instruction set of the Edge TPU. Loading the delegate for the first time takes some time (2.6s)
class run_pose_joint_model():
    def __init__(self):
        #self.interpreter=tflite.Interpreter(FILEPATH_POSE_MODEL_CPU)
        self.interpreter= tflite.Interpreter(model_path=FILEPATH_POSE_MODEL_TPU, experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.interpreter.allocate_tensors()
        self.input=self.interpreter.get_input_details()
        self.output=self.interpreter.get_output_details()
    def run_inference(self,np_array):
        self.interpreter.set_tensor(self.input[0]['index'], np_array)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output[0]['index'])
        return output
#Class for classification model
#With enabling/disabling the first two lines (self.interpreter) it can be selected whether the model should run on CPU or TPU
#For the TPU Models a delegate has to be given as an input parameter for the interpreter. The delegate is required by the interpreter
#to deal with the specific instruction set of the Edge TPU. Loading the delegate for the first time takes some time (2.6s)     
class run_classification_model():
    def __init__(self):
        #self.interpreter=edgetpu.make_interpreter(FILEPATH_CLASSIFICATION_MODEL_TPU)
        self.interpreter=tflite.Interpreter(model_path=FILEPATH_CLASSIFICATION_MODEL_CPU)
        self.interpreter.allocate_tensors()
        self.input=self.interpreter.get_input_details()
        self.output=self.interpreter.get_output_details()
    def run_inference(self,np_array):
        self.interpreter.set_tensor(self.input[0]['index'], np_array)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output[0]['index'])
        return output

def main(args=None):
    rclpy.init(args=args)
    app_node = Inference()
    rclpy.spin(app_node)

    app_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    