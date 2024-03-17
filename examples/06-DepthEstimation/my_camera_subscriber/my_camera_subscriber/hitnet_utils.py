import tensorflow as tf
import tflite_runtime.interpreter as tflite
from tensorflow.lite.python.interpreter import Interpreter
from dataclasses import dataclass
from enum import Enum
import cv2
import numpy as np


@dataclass
class CameraConfig:
    baseline: float
    f: float


class ModelType(Enum):
    eth3d = 0
    middlebury = 1
    flyingthings = 2


class HitNet():
    def __init__(self, model_path, model_type=ModelType.eth3d, camera_config=CameraConfig(0.150, 256*(2.8/6.8)),
                 use_tflite=False):
        self.model_path = model_path
        self.model_type = model_type
        self.camera_config = camera_config
        self.use_tflite = use_tflite

        if use_tflite:
            # Load the TFLite model
            #self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter = Interpreter(model_path=model_path, experimental_delegates=[tflite.load_delegate('/usr/lib/x86_64-linux-gnu/libedgetpu.so.1')])
            self.interpreter.allocate_tensors()

            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        else:
            # Load the SavedModel
            self.model = tf.saved_model.load(model_path)

    def __call__(self, left_img, right_img):
        disparity_map = self.estimate_disparity(left_img, right_img)
        return self.get_depth(disparity_map)

    def prepare_input(self, left_img, right_img):
        if self.use_tflite:
            left_img = cv2.resize(left_img, (256, 256))
            right_img = cv2.resize(right_img, (256, 256))

        if (self.model_type == ModelType.eth3d):
            # Shape (1, None, None, 2)
            left_img = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
            right_img = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

            left_img = np.expand_dims(left_img, 2)
            right_img = np.expand_dims(right_img, 2)
            combined_img = np.concatenate((left_img, right_img), axis=-1) / 255.0
        else:
            # Shape (1, None, None, 6)
            left_img = cv2.cvtColor(left_img, cv2.COLOR_BGR2RGB)
            right_img = cv2.cvtColor(right_img, cv2.COLOR_BGR2RGB)
            combined_img = np.concatenate((left_img, right_img), axis=-1) / 255.0

        return tf.convert_to_tensor(np.expand_dims(combined_img, 0), dtype=tf.float32)


    def get_depth(self, disparity_map):
        return (self.camera_config.f * self.camera_config.baseline) / disparity_map

    def draw_disparity(self, disparity_map):
        disparity_map = disparity_map.astype(np.uint8)
        norm_disparity_map = (
                    255 * ((disparity_map - np.min(disparity_map)) / (np.max(disparity_map) - np.min(disparity_map))))
        return cv2.applyColorMap(cv2.convertScaleAbs(norm_disparity_map, 1), cv2.COLORMAP_MAGMA)

    def draw_depth(self, depth_map, max_dist):
        norm_depth_map = 255 * (1 - depth_map / max_dist)
        norm_depth_map[norm_depth_map < 0] = 0
        norm_depth_map[depth_map == 0] = 0
        return cv2.applyColorMap(cv2.convertScaleAbs(norm_depth_map, 1), cv2.COLORMAP_MAGMA)

    def estimate_disparity(self, left_img, right_img):
        try:
            input_tensor = self.prepare_input(left_img, right_img)
        except ValueError as e:
            print(f"Error preparing input: {str(e)}")
            return None

        if self.use_tflite:
            # Run inference with the TFLite model
            self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
            self.interpreter.invoke()
            disparity_map = self.interpreter.get_tensor(self.output_details[0]['index'])
        else:
            # Run inference with the SavedModel
            print(self.model.signatures.keys())
            output_tensor = self.model.signatures['serving_default'](input_tensor)['reference_output_disparity:0']
            disparity_map = output_tensor.numpy()
        if self.model_type == ModelType.flyingthings:
            left_disparity, right_disparity = disparity_map
            self.disparity_map = left_disparity
        else:
            self.disparity_map = disparity_map

        return disparity_map
