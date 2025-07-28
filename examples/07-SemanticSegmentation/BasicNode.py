import argparse
import time

import rclpy
import torch
from PIL import Image
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from tqdm import tqdm

from segmentation.Segmenter import Segmenter
from utility.BenchmarkManager import BenchmarkManager
from utility.config import (LOGS_FILEPATH, MAX_CORES, MAXIMUM_DIMENSION,
                            OPTIMAL_DIMENSION, THRESHOLD)
from utility.custom_types import InferenceTimings

# CONFIG
INPUT_TOPIC = '/olive/camera/id001/image/compressed'
OUTPUT_TOPIC = '/olive/camera/segmented/image/compressed'


class ImageRelay(Node):
    def __init__(self, benchmarking, fps_active=False, logs_filepath=LOGS_FILEPATH, optimal_dimension=OPTIMAL_DIMENSION,
                 multiple_cores=False):
        super().__init__('image_relay')

        self.get_logger().info('Image relay node started')

        # Subscribe to the TPU-compressed image topic
        self.subscription = self.create_subscription(
            CompressedImage,
            INPUT_TOPIC,
            self.on_image_wrapper,
            qos_profile=rclpy.qos.qos_profile_sensor_data
        )

        self.get_logger().info("Subscription established")

        # Publish the relayed image to the camera topic
        self.publisher = self.create_publisher(
            CompressedImage,
            OUTPUT_TOPIC,
            rclpy.qos.qos_profile_sensor_data
        )

        self.get_logger().info("Publisher established")

        self.latest_im = Image.Image
        # Establishing the models
        self.segmenter = Segmenter(labels_callback=self.labels_callback)

        self.fps = fps_active

        # configuration variables
        self.benchmarking = benchmarking
        if self.benchmarking:
            self.logs_filepath = logs_filepath

            self.get_logger().info("Segmenter Established.")
            self.get_logger().info("Benchmarking Enabled.")
            self.get_logger().debug("Savings logs to: " + self.logs_filepath)
            self.get_logger().info(
                f"Number of Threads: {torch.get_num_threads()}")

            self.benchmarking = benchmarking
            self.latest_labels: set = {0}
            self.shutdown_status = False
            self.index = 0
            self.num_cores = 1
            self.current = optimal_dimension
            self.multiple_cores = multiple_cores

            self.bm = BenchmarkManager(True, False, time.time_ns())

            if self.multiple_cores:
                self.core_pbar = tqdm(total=MAX_CORES, desc="Cores", initial=1)
                torch.set_num_threads(1)

            self.pbar = tqdm(total=(
                #
                int(MAXIMUM_DIMENSION[0] / self.current[0])), desc="Benchmarking Progress")
            self.pbar_small = tqdm(
                total=THRESHOLD, desc="Current Dimension Loop", leave=False)

            self.inference_timings: InferenceTimings = {}
            self.scaling_factor = 1
            self.original_base_dimension = optimal_dimension

            self.get_logger().info(
                f"Camera Resolution: ({self.current[0]} x {self.current[1]})")

    def labels_callback(self, labels: set[int], img: Image):
        """
        Callback function to allow the Segmenter class to report the latest results
        :param labels: Indices of the classes identified in the image frame
        :param img: Segmented PIL image
        :return: None
        """
        self.latest_labels = labels
        self.latest_im = img
        self.latest_im = self.latest_im.convert("RGB")

    def log_data_for_benchmarking(self, total_time: float, labels: set[int]):
        """
        Updates the timings dictionary to keep track of inference times.
        :param total_time: Time for one image inference
        :param labels: An array of integers, corresponding to indices for labels detected in an image frame.
        :return: None
        """
        # Saving each inference timing to its respective dimension
        if (self.current, self.num_cores) in self.inference_timings:
            self.inference_timings[(self.current, self.num_cores)].append(
                (total_time, labels))
        else:
            self.inference_timings[(self.current, self.num_cores)] = [
                (total_time, labels)]

        self.index += 1
        self.pbar_small.update(1)

        # Once enough images have been collected at a specific dimension, move to the next frame size
        if self.index == THRESHOLD:
            self.pbar.update(1)
            self.pbar_small.reset(total=THRESHOLD)
            self.index = 0
            self.scaling_factor += 1
            self.current = (self.original_base_dimension[0] * self.scaling_factor,
                            self.original_base_dimension[1] * self.scaling_factor)
            self.get_logger().debug(
                f"Current Frame Quality: ({self.current[0]}, {self.current[1]})")

            if self.current[0] > MAXIMUM_DIMENSION[0] and self.current[1] > MAXIMUM_DIMENSION[1]:
                if not self.multiple_cores:
                    self.get_logger().info("Max quality reached, shutting down...")
                    self.shutdown_status = True
                else:
                    if self.num_cores == MAX_CORES:
                        self.get_logger().info("Max quality reached, shutting down...")
                        self.shutdown_status = True
                    else:
                        self.current = self.original_base_dimension
                        self.scaling_factor = 1

                        self.num_cores += 1
                        torch.set_num_threads(self.num_cores)

                        self.pbar.reset(
                            total=(int(MAXIMUM_DIMENSION[0] / self.original_base_dimension[0])))
                        self.core_pbar.update(1)

    def on_image_wrapper(self, msg: CompressedImage):
        """
        Wrapper function to allow the Segmenter image function to be benchmarked
        :param msg: CompressedImage from the ROS 2 camera data stream
        :return: None
        """

        start = time.perf_counter()
        result = self.segmenter.on_image(msg, downsize=False)
        total_time = time.perf_counter() - start

        if self.fps:
            self.get_logger().info(f"FPS: {(1.0 / total_time):.2f}")

        if self.benchmarking:
            self.log_data_for_benchmarking(
                total_time=total_time, labels=self.latest_labels)

            if self.shutdown_status:
                self.destroy_node()

        self.publisher.publish(result)
        self.get_logger().debug("Relayed one image frame")

    def cleanup(self):
        """
        End of life function that manages log file saving, progress bar closing if benchmarking is active.
        :return: None
        """
        if self.benchmarking:
            self.bm.save_to_file(self.inference_timings)
            self.bm.generate_yaml(time.time_ns())
            # save_to_file(self.inference_timings, self.logs_filepath)
            self.pbar.close()
            self.pbar_small.close()

            if self.multiple_cores:
                self.core_pbar.close()
            self.get_logger().info("Segmenter cleanup done. Destroying node...")


def main():
    parser = argparse.ArgumentParser(
        prog='3D Segmentation',
        description='This activates a node to run image segmentation',
        epilog='For more help, please see the README and other relevant documentation.')

    parser.add_argument('-b', '--benchmark', type=str,
                        help='Enable benchmarking mode')
    parser.add_argument('-c', '--cores', action='store_true',
                        help='Enable benchmarking across cores')
    parser.add_argument('-f', '--fps', action='store_true',
                        help='Enable FPS tracking mode')
    args = parser.parse_args()

    rclpy.init()

    benchmarking_active = args.benchmark is not None
    benchmark_name = args.benchmark if args.benchmark else "default"

    node = ImageRelay(benchmarking=benchmarking_active,
                      fps_active=args.fps,
                      logs_filepath=benchmark_name + "_" + LOGS_FILEPATH,
                      multiple_cores=args.cores)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("KeyboardInterrupt received. Shutting down...")
    finally:
        # Save log files
        if benchmarking_active:
            node.cleanup()

        # ROS 2 Cleanup
        node.destroy_node()
        if rclpy.ok():
            node.get_logger().info("Shutting down ROS...")
            rclpy.shutdown()


if __name__ == '__main__':
    main()
