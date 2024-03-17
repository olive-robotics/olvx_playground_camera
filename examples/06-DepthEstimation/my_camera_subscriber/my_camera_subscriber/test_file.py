from tensorflow.lite.python.interpreter import Interpreter
import tensorflow as tf
import cv2
import numpy as np
import time
import glob
from matplotlib import gridspec
from matplotlib import pyplot as plt

LABEL_NAMES = np.asarray([
    'road',
    'sidewalk',
    'building',
    'wall',
    'fence',
    'pole',
    'traffic light',
    'traffic sign',
    'vegetation',
    'terrain',
    'sky',
    'person',
    'rider',
    'car',
    'truck',
    'bus',
    'train',
    'motorcycle',
    'bicycle',
])

FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)

left_images = glob.glob(
    '/home/malek/PycharmProjects/MA_Malek/ma_malek_camera_neural_depth_estimation/frames_cleanpass_webp/35mm_focallength/scene_forwards/fast/left/*.webp')
left_images.sort()
right_images = glob.glob(
    '/home/malek/PycharmProjects/MA_Malek/ma_malek_camera_neural_depth_estimation/frames_cleanpass_webp/35mm_focallength/scene_forwards/fast/left/*.webp')
right_images.sort()
depth_images = glob.glob(
    '/home/malek/PycharmProjects/MA_Malek/ma_malek_camera_neural_depth_estimation/tflite_stereo_depth_estimation/DrivingStereo_images/depth/*.png')
depth_images.sort()


class RealtimeStereo():
    def __init__(self, model_path):
        self.output_shape = None
        self.output_details = None
        self.channels = None
        self.input_width = None
        self.input_height = None
        self.input_details = None
        self.interpreter = None
        self.load_model(model_path)

    def load_model(self, model_path):
        self.interpreter = Interpreter(model_path, num_threads=4)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        input_shape = self.input_details[0]['shape']
        self.input_height = input_shape[1]
        self.input_width = input_shape[2]
        self.channels = input_shape[2]

        self.output_details = self.interpreter.get_output_details()
        self.output_shape = self.output_details[0]['shape']

    """def preprocess(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_input = cv2.resize(
            img,
            (self.input_width,self.input_height)
        ).astype(np.float32)

        # Scale input pixel values to -1 to 1
        mean=[0.485, 0.456, 0.406]
        std=[0.229, 0.224, 0.225]
        img_input = ((img_input/ 255.0 - mean) / std)
        # img_input = img_input.transpose(2, 0, 1)
        img_input = img_input[np.newaxis,:,:,:]

        return img_input.astype(np.float32)"""

    def preprocess(self, image):
        # Convert from BGR to RGB
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Calculate required padding
        if img.shape[0] % 16 != 0:
            times = img.shape[0] // 16
            top_pad = (times + 1) * 16 - img.shape[0]
        else:
            top_pad = 0

        if img.shape[1] % 16 != 0:
            times = img.shape[1] // 16
            right_pad = (times + 1) * 16 - img.shape[1]
        else:
            right_pad = 0

        # Pad the original image
        img_padded = cv2.copyMakeBorder(img, top_pad, 0, 0, right_pad, cv2.BORDER_CONSTANT, value=(0, 0, 0))

        # Resize the padded image to the model's expected dimensions
        img_resized = cv2.resize(img_padded, (self.input_width, self.input_height)).astype(np.float32)

        # Normalize the image
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        img_normalized = ((img_resized / 255.0 - mean) / std)

        # Add batch dimension
        img_input = img_normalized[np.newaxis, :, :, :]

        return img_input.astype(np.float32)

    def run(self, left, right):
        input_left = self.preprocess(left)
        input_right = self.preprocess(right)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_left)
        self.interpreter.set_tensor(self.input_details[1]['index'], input_right)
        self.interpreter.invoke()

        disparity = self.interpreter.get_tensor(self.output_details[0]['index'])

        return np.squeeze(disparity)

    def get_segmentation_mask(self, image):
        model_path = '/home/malek/PycharmProjects/MA_Malek/ma_malek_camera_neural_depth_estimation/deepLabV3+/lite-model_deeplabv3_1_metadata_2.tflite'
        segmentation_interpreter = Interpreter(model_path, num_threads=4)
        segmentation_interpreter.allocate_tensors()
        segmentation_input_details = segmentation_interpreter.get_input_details()
        segmentation_output_details = segmentation_interpreter.get_output_details()
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_input = cv2.resize(img, (
            segmentation_input_details[0]['shape'][2], segmentation_input_details[0]['shape'][1])).astype(np.float32)
        img_input = img_input[np.newaxis, :, :, :]
        segmentation_interpreter.set_tensor(segmentation_input_details[0]['index'], img_input)
        segmentation_interpreter.invoke()
        # Preprocess the image for the model
        output_array = segmentation_interpreter.get_tensor(segmentation_output_details[0]['index'])
        # Ensure the segmentation output is 2D
        seg_map = np.argmax(output_array[0], axis=-1)
        color_coded_mask = self.label_to_color_image(seg_map)
        return color_coded_mask, seg_map

    def create_cityscapes_label_colormap(self):
        """Creates a label colormap used in CITYSCAPES segmentation benchmark.
      Returns:
        A colormap for visualizing segmentation results.
      """
        colormap = np.zeros((256, 3), dtype=np.uint8)
        colormap[0] = [128, 64, 128]
        colormap[1] = [244, 35, 232]
        colormap[2] = [70, 70, 70]
        colormap[3] = [102, 102, 156]
        colormap[4] = [190, 153, 153]
        colormap[5] = [153, 153, 153]
        colormap[6] = [250, 170, 30]
        colormap[7] = [220, 220, 0]
        colormap[8] = [107, 142, 35]
        colormap[9] = [152, 251, 152]
        colormap[10] = [70, 130, 180]
        colormap[11] = [220, 20, 60]
        colormap[12] = [255, 0, 0]
        colormap[13] = [0, 0, 142]
        colormap[14] = [0, 0, 70]
        colormap[15] = [0, 60, 100]
        colormap[16] = [0, 80, 100]
        colormap[17] = [0, 0, 230]
        colormap[18] = [119, 11, 32]
        return colormap

    def label_to_color_image(self, label):
        """Adds color defined by the dataset colormap to the label.

      Args:
        label: A 2D array with integer type, storing the segmentation label.

      Returns:
        result: A 2D array with floating type. The element of the array
          is the color indexed by the corresponding element in the input label
          to the PASCAL color map.

      Raises:
        ValueError: If label is not of rank 2 or its value is larger than color
          map maximum entry.
      """
        if label.ndim != 2:
            raise ValueError('Expect 2-D input label')

        colormap = self.create_cityscapes_label_colormap()

        if np.max(label) >= len(colormap):
            raise ValueError('label value too large.')

        return colormap[label]

    """def vis_segmentation(self, image, seg_map):
      Visualizes input image, segmentation map and overlay view.
      FULL_COLOR_MAP = self.label_to_color_image(FULL_LABEL_MAP)

      plt.figure(figsize=(15, 5))
      grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

      plt.subplot(grid_spec[0])
      plt.imshow(image)
      plt.axis('off')
      plt.title('input image')

      plt.subplot(grid_spec[1])
      seg_image = self.label_to_color_image(seg_map).astype(np.uint8)
      plt.imshow(seg_image)
      plt.axis('off')
      plt.title('segmentation map')

      plt.subplot(grid_spec[2])
      plt.imshow(image)
      plt.imshow(seg_image, alpha=0.7)
      plt.axis('off')
      plt.title('segmentation overlay')

      unique_labels = np.unique(seg_map)
      ax = plt.subplot(grid_spec[3])
      plt.imshow(
          FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
      ax.yaxis.tick_right()
      plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
      plt.xticks([], [])
      ax.tick_params(width=0.0)
      plt.grid('off')
      plt.show()"""

    def vis_segmentation(self, image, seg_map):
        """Visualizes input image, segmentation map, and overlay view using OpenCV."""

        # Convert PIL image to numpy array
        image_np = np.array(image)

        # Get color-coded segmentation image
        seg_image = self.label_to_color_image(seg_map).astype(np.uint8)

        # Resize seg_image to match image_np's dimensions
        seg_image_resized = cv2.resize(seg_image, (image_np.shape[1], image_np.shape[0]))

        # Ensure both images are 3-channel images
        if image_np.shape[2] == 1:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        if seg_image_resized.shape[2] == 1:
            seg_image_resized = cv2.cvtColor(seg_image_resized, cv2.COLOR_GRAY2BGR)

        # Overlay the segmentation image on the original image
        overlay = cv2.addWeighted(image_np, 0.6, seg_image_resized, 0.4, 0)

        # Display the images
        cv2.imshow('Input Image', image_np)
        cv2.imshow('Segmentation Map', seg_image_resized)
        cv2.imshow('Segmentation Overlay', overlay)

        # This will display the image for 1 ms
        cv2.waitKey(1)


if __name__ == '__main__':
    # model_path = 'saved_model/model_float32.tflite'
    model_path = '/home/malek/PycharmProjects/MA_Malek/ma_malek_camera_neural_depth_estimation/stereo_depth_model/realtime480x640_float32.tflite'
    # model_path = 'saved_model/model_dynamic_range_quant.tflite'
    realtimeStereo = RealtimeStereo(model_path)

    # img_left = cv2.imread('im0.png')
    # img_right = cv2.imread('im1.png')

    """start = time.time()

    disp = realtimeStereo.run(img_left, img_right)

    disp = cv2.resize(
        disp,
        (img_left.shape[1], img_left.shape[0]),
        interpolation=cv2.INTER_LINEAR
    ).astype(np.float32)
    img = (disp*256).astype('uint32')
    cv2.imshow('disp', img)

    d_min = np.min(disp)
    d_max = np.max(disp)
    depth_map = (disp - d_min) / (d_max - d_min)
    depth_map = depth_map * 255.0
    depth_map = np.asarray(depth_map, dtype="uint8")
    depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)

    end = time.time()
    eslapse = end - start
    print("depthmap : {}s".format(eslapse))

    cv2.imwrite('result.jpg', depth_map)

    cv2.imshow('output', depth_map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    for left_path, right_path, depth_path in zip(left_images, right_images, depth_images):

        # Read frame from the video
        left_img = cv2.imread(left_path)
        right_img = cv2.imread(right_path)
        depth_img = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED).astype(np.float32) / 256
        start = time.time()
        # Added part for the segmentation
        # Combine the left and right images
        combined_img = np.concatenate((left_img, right_img), axis=1)
        # Get the color-coded segmentation mask for the left image
        segmentation_mask_left, seg_map = realtimeStereo.get_segmentation_mask(left_img)
        # Ensure the segmentation mask is the same size as the left_img
        segmentation_mask_left_resized = cv2.resize(segmentation_mask_left, (left_img.shape[1], left_img.shape[0]))
        realtimeStereo.vis_segmentation(left_img, seg_map)
        # Now overlay the images
        overlay_left = cv2.addWeighted(left_img, 0.35, segmentation_mask_left_resized, 0.65, 0)

        # cv2.imshow("Overlay Left Image", overlay_left)
        # Estimate the depth
        disparity_map = realtimeStereo.run(left_img, right_img)
        masked_disparity_map_left = disparity_map
        disparity_map = cv2.resize(
            disparity_map,
            (left_img.shape[1], left_img.shape[0]),
            interpolation=cv2.INTER_LINEAR
        ).astype(np.float32)
        img = (disparity_map * 256).astype('uint16')
        d_min = np.min(disparity_map)
        d_max = np.max(disparity_map)
        depth_map = (disparity_map - d_min) / (d_max - d_min)
        depth_map = depth_map * 255.0
        """if segmentation_mask_right.size != 0:
            # Resize the segmentation mask
            segmentation_mask_right_resized = cv2.resize(segmentation_mask_right, (depth_map.shape[1], depth_map.shape[0]), interpolation=cv2.INTER_NEAREST)
            segmentation_mask_right_resized = segmentation_mask_right_resized.astype(np.float32)

            # Apply the car mask
            car_mask_right = np.where(segmentation_mask_right_resized == 26, 1, 0)
            depth_map = np.asarray(depth_map, dtype="uint8")
            depth_map = cv2.applyColorMap(depth_map * car_mask_right, cv2.COLORMAP_MAGMA)"""
        depth_map = np.asarray(depth_map, dtype="uint8")
        depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_MAGMA)
        # depth_map = cv2.LUT(depth_map, LUT)
        end = time.time()
        eslapse = end - start

        # color_disparity = draw_disparity(disparity_map)
        # color_depth = draw_depth(depth_map, max_distance)
        # color_real_depth = draw_depth(depth_img, max_distance)

        # color_depth = cv2.resize(color_depth, (left_img.shape[1],left_img.shape[0]))
        # depth_map_3ch = cv2.cvtColor(depth_map, cv2.COLOR_GRAY2BGR)
        cobined_image = np.hstack((left_img, depth_map))

        # out.write(cobined_image)
        cv2.imshow("Estimated depth", cobined_image)
        cv2.imshow("Estimated disparity", disparity_map)
        # Press key q to stop
        if cv2.waitKey(1) == ord('q'):
            break

# Retrieve the JET colormap and reverse it
"""     colormap = cv2.applyColorMap(np.arange(0, 256, 1, dtype=np.uint8).reshape(256, 1), cv2.COLORMAP_JET).squeeze()
reversed_colormap = np.flipud(colormap)
LUT = np.zeros((256, 1, 3), dtype=np.uint8)
LUT[:, 0, :] = reversed_colormap
depth_map_3ch = cv2.cvtColor(depth_map, cv2.COLOR_GRAY2BGR)
depth_map = cv2.LUT(depth_map_3ch, LUT)"""
