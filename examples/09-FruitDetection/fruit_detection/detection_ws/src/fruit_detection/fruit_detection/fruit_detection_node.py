# Copyright 2024 Ekumen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides a ros2 detection node for a fasterrcnn_resnet50_fpn model."""

import rclpy
from rclpy.node import Node
from rclpy.qos import (
    HistoryPolicy,
    QoSProfile,
    ReliabilityPolicy,
)
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import Header
from vision_msgs.msg import (
    BoundingBox2D,
    Detection2D,
    Detection2DArray,
    ObjectHypothesis,
    ObjectHypothesisWithPose,
)
from cv_bridge import CvBridge
import cv2
import torch
from torchvision import transforms as T
from torchvision.models.detection.faster_rcnn import (
    FastRCNNPredictor,
    fasterrcnn_resnet50_fpn,
)
import time

_FRUIT_CATEGORIES = {
    0: "background",
    1: "apple",
    2: "avocado",
    3: "lime",
}


def get_transform():
    """Return a PyTorch transform callable object."""
    transforms = []
    transforms.append(T.ToPILImage())
    transforms.append(T.PILToTensor())
    transforms.append(T.ConvertImageDtype(torch.float))
    return T.Compose(transforms)


class FruitDetectionNode(Node):
    """
    Inference node for fruit detection.

    Reads images from /image_raw and publishes another image
    into /proc_image with detections made with a fasterrcnn_resnet50_fpn model.
    On top of that, it publishes the bounding box of the detections to
    /detections.
    """

    TARGET_ENCODING = "bgr8"
    TOPIC_QOS_QUEUE_LENGTH = 2
    OLIVE_CAMERA_QOS_PROFILE = QoSProfile(
        reliability=ReliabilityPolicy.RELIABLE,
        history=HistoryPolicy.KEEP_LAST,
        depth=TOPIC_QOS_QUEUE_LENGTH,
    )
    PROC_QOS_PROFILE = QoSProfile(
        reliability=ReliabilityPolicy.RELIABLE,
        history=HistoryPolicy.KEEP_LAST,
        depth=TOPIC_QOS_QUEUE_LENGTH,
    )
    RECT_COLOR = (0, 0, 255)
    LOGGING_THROTTLE = 1.0
    MINIMUM_BBOX_SIZE_X = 0
    MINIMUM_BBOX_SIZE_Y = 0
    MAXIMUM_BBOX_SIZE_X = 640
    MAXIMUM_BBOX_SIZE_Y = 480
    MINIMUM_SCORE_THRESHOLD = 0.0
    MAXIMUM_SCORE_THRESHOLD = 1.0

    def __init__(self) -> None:
        """Initialize the node."""
        super().__init__("detection_node")
        self.declare_parameter("model_path", "model.pth")
        self.declare_parameter("webcam_topic", "/image_raw")
        self.declare_parameter(
            "olive_camera_topic", "/olive/camera/id01/image/compressed"
        )
        self.declare_parameter("bbox_min_x", 60)
        self.declare_parameter("bbox_min_y", 60)
        self.declare_parameter("bbox_max_x", 200)
        self.declare_parameter("bbox_max_y", 200)
        self.declare_parameter("score_threshold", 0.9)
        self.add_on_set_parameters_callback(self.validate_parameters)

        self.__model_path = (
            self.get_parameter("model_path").get_parameter_value().string_value
        )
        self.__webcam_topic = (
            self.get_parameter("webcam_topic")
            .get_parameter_value()
            .string_value  # noqa: E501
        )
        self.__olive_camera_topic = (
            self.get_parameter("olive_camera_topic")
            .get_parameter_value()
            .string_value  # noqa: E501
        )

        self.webcam_image_subscription = self.create_subscription(
            Image,
            self.__webcam_topic,
            self.webcam_image_callback,
            FruitDetectionNode.TOPIC_QOS_QUEUE_LENGTH,
        )
        self.olive_camera_image_subscription = self.create_subscription(
            CompressedImage,
            self.__olive_camera_topic,
            self.olive_image_callback,
            FruitDetectionNode.OLIVE_CAMERA_QOS_PROFILE,
        )

        self.image_publisher = self.create_publisher(
            Image, "/proc_image", FruitDetectionNode.PROC_QOS_PROFILE
        )
        self.detections_publisher = self.create_publisher(
            Detection2DArray,
            "/detections",
            FruitDetectionNode.PROC_QOS_PROFILE,
        )
        self.cv_bridge = CvBridge()
        self.device_str = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(self.device_str)
        self.load_model()
        self.get_logger().info(
            f" device? {self.device_str} version {torch.__version__}"
        )
        # Provides CSV column format for the time measurements.
        self.get_logger().info("ingestion;inference;plot;detection;publish;")
        self.ingest_transform = get_transform()

    def validate_parameters(self, params):
        """
        Validate parameter changes.

        Args:
        -----
            params (list[Parameter]): list of parameters to analyze.

        Returns:
        --------
            SetParametersResult with the result of the analysis
        """
        is_valid = True
        reason = ""
        for param in params:
            if param.name == "bbox_min_x":
                if param.type_ != Parameter.Type.INTEGER or not (
                    FruitDetectionNode.MINIMUM_BBOX_SIZE_X
                    <= param.value
                    <= FruitDetectionNode.MAXIMUM_BBOX_SIZE_X
                ):
                    is_valid = False
                    reason = (
                        "bbox_min_x: is not in range ["
                        f"{FruitDetectionNode.MINIMUM_BBOX_SIZE_X}; "
                        f"{FruitDetectionNode.MAXIMUM_BBOX_SIZE_X}]"
                    )
                    break
                else:
                    reason = "bbox_min_x successfully set."
            elif param.name == "bbox_min_y":
                if param.type_ != Parameter.Type.INTEGER or not (
                    FruitDetectionNode.MINIMUM_BBOX_SIZE_Y
                    <= param.value
                    <= FruitDetectionNode.MAXIMUM_BBOX_SIZE_Y
                ):
                    is_valid = False
                    reason = (
                        "bbox_min_y: is not in range ["
                        f"{FruitDetectionNode.MINIMUM_BBOX_SIZE_Y}; "
                        f"{FruitDetectionNode.MAXIMUM_BBOX_SIZE_Y}]"
                    )
                    break
                else:
                    reason = "bbox_min_y successfully set."
            if param.name == "bbox_max_x":
                if param.type_ != Parameter.Type.INTEGER or not (
                    FruitDetectionNode.MINIMUM_BBOX_SIZE_X
                    <= param.value
                    <= FruitDetectionNode.MAXIMUM_BBOX_SIZE_X
                ):
                    is_valid = False
                    reason = (
                        "bbox_max_x: is not in range ["
                        f"{FruitDetectionNode.MINIMUM_BBOX_SIZE_X}; "
                        f"{FruitDetectionNode.MAXIMUM_BBOX_SIZE_X}]"
                    )
                    break
                else:
                    reason = "bbox_max_x successfully set."
            elif param.name == "bbox_max_y":
                if param.type_ != Parameter.Type.INTEGER or not (
                    FruitDetectionNode.MINIMUM_BBOX_SIZE_Y
                    <= param.value
                    <= FruitDetectionNode.MAXIMUM_BBOX_SIZE_Y
                ):
                    is_valid = False
                    reason = (
                        "bbox_max_y: is not in range ["
                        f"{FruitDetectionNode.MINIMUM_BBOX_SIZE_Y}; "
                        f"{FruitDetectionNode.MAXIMUM_BBOX_SIZE_Y}]"
                    )
                    break
                else:
                    reason = "bbox_max_y successfully set."
            elif param.name == "score_threshold":
                if param.type_ != Parameter.Type.DOUBLE or not (
                    FruitDetectionNode.MINIMUM_SCORE_THRESHOLD
                    <= param.value
                    <= FruitDetectionNode.MAXIMUM_SCORE_THRESHOLD
                ):
                    is_valid = False
                    reason = (
                        "score_threshold: is not in range ["
                        f"{FruitDetectionNode.MINIMUM_SCORE_THRESHOLD}; "
                        f"{FruitDetectionNode.MAXIMUM_SCORE_THRESHOLD}]"
                    )
                    break
        if not is_valid:
            self.get_logger().warn(f"Skipping to set parameter: {reason}")
        return SetParametersResult(successful=is_valid, reason=reason)

    def load_model(self):
        """Load the torch model."""
        self.model = fasterrcnn_resnet50_fpn(weights=None)
        in_features = self.model.roi_heads.box_predictor.cls_score.in_features
        self.model.roi_heads.box_predictor = FastRCNNPredictor(
            in_features, len(_FRUIT_CATEGORIES)
        )
        self.model = self.model.to(self.device)
        self.model.load_state_dict(
            torch.load(
                self.__model_path,
                weights_only=True,
            )
        )
        self.model.eval()
        self._labels = _FRUIT_CATEGORIES

    def image_to_tensor(self, img):
        """Apply transforms to a cv2 image."""
        transformed_img = self.ingest_transform(img)
        return [transformed_img.to(self.device)]

    def cv2_to_torch_frame(self, img):
        """Prepare cv2 image for inference."""
        return self.image_to_tensor(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    def bbox_is_in_range(self, box, min_x, min_y, max_x, max_y):
        """
        Check if a box is within size.

        Args:
        -----
            box (tuple[int, int, int, int]): bounding box from inference.
            min_x (int): minimum horizontal length of the bounding box.
            min_y (int): minimum vertical length of the bounding box.
            max_x (int): maximum horizontal length of the bounding box.
            max_y (int): maximum vertical length of the bounding box.

        Returns:
        --------
            bool True if the box size is in range.
        """
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        dx = x2 - x1
        dy = y2 - y1
        return (min_x <= dx <= max_x) and (min_y <= dy <= max_y)

    def score_frame(self, frame):
        """
        Score each frame of the video and return results.

        Args:
        -----
            frame (cv2.Mat): frame to be infered.

        Returns:
        --------
            list[dict] labels and coordinates of objects found.
        """
        with torch.no_grad():
            output = self.model(frame)
            # As we only feed one image, we should get only one output
            output = output[0]
            results = []
            for i, (box, score, label) in enumerate(
                zip(output["boxes"], output["scores"], output["labels"])
            ):
                bbox_min_x = (
                    self.get_parameter("bbox_min_x")
                    .get_parameter_value()
                    .integer_value  # Minimum bbox x size
                )
                bbox_min_y = (
                    self.get_parameter("bbox_min_y")
                    .get_parameter_value()
                    .integer_value  # Minimum bbox y size
                )
                bbox_max_x = (
                    self.get_parameter("bbox_max_x")
                    .get_parameter_value()
                    .integer_value  # Maximum bbox x size
                )
                bbox_max_y = (
                    self.get_parameter("bbox_max_y")
                    .get_parameter_value()
                    .integer_value  # Maximum bbox y size
                )
                score_threshold = (
                    self.get_parameter("score_threshold")
                    .get_parameter_value()
                    .double_value  # Score threshold
                )
                if score >= score_threshold and self.bbox_is_in_range(
                    box, bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y
                ):
                    results.append(
                        {
                            "box": box,
                            "score": score,
                            "label": self._labels[label.item()],
                        }
                    )
        return results

    def plot_boxes(self, detections, frame) -> None:
        """
        Plot boxes and labels on frame.

        Operations ran on the input frame.

        Args:
        -----
            detections (list[dict]): inferences made by model
            frame (cv2.Mat): frame on which to  make the plots
        """
        for detection in detections:
            row = detection["box"]
            x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                FruitDetectionNode.RECT_COLOR,
                1,
            )
            cv2.putText(
                frame,
                str(detection["label"]),
                (x1, y1),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                1,
            )

    def detection_to_ros2(
        self, detections: list[dict], header: Header
    ) -> Detection2DArray:
        """
        Create a detection result as if there where multiple classes.

        Notes: there are multiple values hardcoded. It is expected to evolve
        the method into something that relates to the actual classes in the
        future. Also, the score in the hyphotesis.
        Provided that there is no pose estimation, only the bounding box is
        given.

        Args:
        -----
            detections (list[dict]): The list of detections to include.
            header (Header): The header stamp of the message to return.

        Returns:
        --------
            Detection2DArray: The detection array with the mulitple detections
                when found.
        """
        result = Detection2DArray()
        result.header = header
        result.detections = []
        for detection in detections:
            x1, y1, x2, y2 = detection["box"]
            detection_2d = Detection2D()
            detection_2d.header = header
            bbox = BoundingBox2D()
            bbox.size_x = float(x2 - x1)
            bbox.size_y = float(y2 - y1)
            bbox.center.theta = 0.0
            bbox.center.position.y = float(y2 - y1) / 2.0
            bbox.center.position.y = float(y2 - y1) / 2.0
            detection_2d.bbox = bbox
            detection_2d.id = detection["label"]
            object_hypothesis_with_pose = ObjectHypothesisWithPose()
            object_hypothesis = ObjectHypothesis()
            object_hypothesis.class_id = detection["label"]
            object_hypothesis.score = float(detection["score"])
            object_hypothesis_with_pose.hypothesis = object_hypothesis
            detection_2d.results.append(object_hypothesis_with_pose)
            result.detections.append(detection_2d)
        return result

    def webcam_image_callback(self, msg: Image) -> None:
        """
        Image callback from the webcam.

        Converts the msg into a header and cv image and forwards
        to the processing function.

        Args:
        -----
            msg (Image): Received image.
        """
        msg_header = msg.header
        cv_frame = self.cv_bridge.imgmsg_to_cv2(
            msg, desired_encoding=FruitDetectionNode.TARGET_ENCODING
        )
        self.image_callback(msg_header, cv_frame)

    def olive_image_callback(self, msg: CompressedImage) -> None:
        """
        Image callback from the Olive Camera.

        Converts the msg into a header and cv image and forwards
        to the processing function.

        Args:
        -----
            msg (Image): Received image.
        """
        msg_header = msg.header
        cv_frame = self.cv_bridge.compressed_imgmsg_to_cv2(
            msg, desired_encoding=FruitDetectionNode.TARGET_ENCODING
        )
        self.image_callback(msg_header, cv_frame)

    def image_callback(self, msg_header: Header, cv_frame) -> None:
        """
        Image callback.

        Produces the detection output together with the annotated image.

        Args:
        -----
            msg_header (Header): Received header.
            cv_frame (Image): Received cv image.
        """
        ingestion_start_time = time.perf_counter()
        torch_frame = self.cv2_to_torch_frame(cv_frame)
        ingestion_end_time = time.perf_counter()

        inference_start_time = time.perf_counter()
        detections = self.score_frame(torch_frame)
        inference_end_time = time.perf_counter()

        plot_start_time = time.perf_counter()
        self.plot_boxes(detections, cv_frame)
        plot_end_time = time.perf_counter()

        detection_start_time = time.perf_counter()
        detections_msg = self.detection_to_ros2(detections, msg_header)
        detection_end_time = time.perf_counter()

        publish_start_time = time.perf_counter()
        self.image_publisher.publish(
            self.cv_bridge.cv2_to_imgmsg(
                cv_frame,
                encoding=FruitDetectionNode.TARGET_ENCODING,
                header=msg_header,
            )
        )
        self.detections_publisher.publish(detections_msg)
        publish_end_time = time.perf_counter()

        log_str = (
            f"{ingestion_end_time - ingestion_start_time};"
            f"{inference_end_time - inference_start_time};"
            f"{plot_end_time-plot_start_time};"
            f"{detection_end_time-detection_start_time};"
            f"{publish_end_time-publish_start_time};"
        )
        self.get_logger().info(
            log_str, throttle_duration_sec=FruitDetectionNode.LOGGING_THROTTLE
        )


def main(args=None) -> None:
    """Run the node."""
    rclpy.init(args=args)
    node = FruitDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
