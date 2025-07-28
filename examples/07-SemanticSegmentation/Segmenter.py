from typing import TYPE_CHECKING

import numpy as np
import torch
from PIL import Image
from transformers import (SegformerForSemanticSegmentation,
                          SegformerImageProcessor)

from utility.config import OPTIMAL_DIMENSION
from utility.image_utility import (bytes_to_im, get_palette, im_to_bytes,
                                   overlay_mask)

if TYPE_CHECKING:
    from sensor_msgs.msg import CompressedImage

# Configuration Variables
MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"


# This class handles the entire image segmentation pipeline.
class Segmenter:
    def __init__(self, dimension=OPTIMAL_DIMENSION, labels_callback=None):
        """
        Initializes the Segmenter and sets up the configuration
        :param dimension: Dimensions to use for image downscaling
        :param labels_callback: Optional function to handle the labels
        """
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')

        # Load model
        self.processor = SegformerImageProcessor.from_pretrained(MODEL_NAME)
        self.model = SegformerForSemanticSegmentation.from_pretrained(
            MODEL_NAME).to(self.device)

        # Prepare palette
        self.num_labels = self.model.config.num_labels
        self.palette = get_palette(num_classes=self.num_labels)

        self.labels_callback = labels_callback
        self.current = dimension

    def on_image(self, msg: "CompressedImage", downsize=True) -> "CompressedImage":
        """
        Wrapper function to run the segmentation code with or without benchmarking enabled.
        :param msg: CompressedImage, the raw stream of data from subscribing to the ROS2 topic
        :return: -1, if the system wants to shut down (only applicable in benchmarking). Otherwise, the image data.
        """

        im = bytes_to_im(msg)
        segmented = self.segment_image(im, downsize=downsize)

        msg.data = im_to_bytes(segmented)
        msg.format = "jpeg"

        return msg

    def segment_image(self, pil_image: Image, downsize: bool = False) -> Image:
        """
        Runs the image segmentation model to edit the ROS 2 CompressedImage message in place.
        :param downsize: Whether or not the function should scale the image down further
        :param pil_image: PIL Image to manipulate
        :return: A PIL.Image with a segmentation mask overlaid
        """

        # Image downscaling
        # downscales image to accelerate model inference
        if downsize:
            pil_image.thumbnail(self.current)

        # run manipulation
        frame = np.array(pil_image)
        inputs = self.processor(
            images=frame, return_tensors="pt").to(self.device)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            mask = logits.argmax(dim=1)[0].cpu().numpy().astype(np.uint8)
        overlay = overlay_mask(frame, mask, self.palette, alpha=0.5)

        # Convert overlay back to PIL image
        overlay_pil = Image.fromarray(overlay)

        if self.labels_callback:
            self.labels_callback(set(np.unique(mask)), overlay_pil)

        return overlay_pil
