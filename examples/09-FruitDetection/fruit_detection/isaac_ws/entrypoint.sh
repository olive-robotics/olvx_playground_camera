#!/usr/bin/bash

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

SIM_SCRIPT_PATH="/root/isaac_ws/simulation_ws/scripts/launch_sim.py"
SDG_SCRIPT_PATH="/root/isaac_ws/simulation_ws/scripts/launch_sdg.py"
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/isaac-sim/exts/omni.isaac.ros2_bridge/humble/lib

SCRIPT_PATH=$(case "${MODE}" in
    "SIM") echo "${SIM_SCRIPT_PATH}" ;;
    "SDG") echo "${SDG_SCRIPT_PATH}" ;;
    *) echo "${SIM_SCRIPT_PATH}" ;;
esac)

cd /isaac-sim

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}

./python.sh ${SCRIPT_PATH}
