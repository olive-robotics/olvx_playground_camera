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

"""Launch the fruit detection node."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Launch description to initiate the detection node.

    ----
    Returns:
        LaunchDescription: With just the fruit_detection_node.
    """
    params_filepath = os.path.join(
        get_package_share_directory("fruit_detection"), "config", "params.yml"
    )
    print(params_filepath)
    ld = LaunchDescription()
    fruit_detection_node = Node(
        package="fruit_detection",
        executable="fruit_detection_node",
        parameters=[params_filepath],
    )
    ld.add_action(fruit_detection_node)
    return ld
