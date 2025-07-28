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

"""Launch Isaac simulation."""

# This is the first thing we need to import per Isaac's documentation.
from isaacsim import SimulationApp

# Configurations
HEADLESS = False
SIMULATION_APP_CONFIG = {
    "headless": HEADLESS,
}
USD_FILE_PATH = "/root/isaac_ws/simulation_ws/scene/scene.usda"
PHYSICS_DT = 1.0 / 40.0
RENDERING_DT = 1.0 / 20.0
STAGE_UNITS_PER_METER = 1.0


def create_sim_app():
    """Create the simulation app."""
    return SimulationApp(SIMULATION_APP_CONFIG)


def config_and_open_stage():
    """Set up and open the stage."""
    from omni.isaac.core.utils.stage import (
        is_stage_loading,
        open_stage,
    )

    open_stage(USD_FILE_PATH)
    while is_stage_loading():
        pass


def create_and_configure_context():
    """Create and configure the simulation context."""
    from omni.isaac.core import SimulationContext

    simulation_context = SimulationContext(
        physics_dt=PHYSICS_DT,
        rendering_dt=RENDERING_DT,
        stage_units_in_meters=STAGE_UNITS_PER_METER,
    )
    simulation_context.initialize_physics()
    return simulation_context


def enable_extensions():
    """Enable required extentsions."""
    from omni.isaac.core.utils.extensions import enable_extension

    enable_extension("omni.isaac.ros2_bridge")


# Create the simulation application.
simulation_app = create_sim_app()

# Open a stage and load the USD file. Wait for the stage to finish loading.
config_and_open_stage()

# Enable the extensions required for the system to work.
enable_extensions()

# Create a simulation context for the simulated application,
# and initialize the physics.
simulation_context = create_and_configure_context()

# Execute the simulation by ticking it.
simulation_context.play()
while simulation_app.is_running():
    simulation_app.update()

# Terminate the simulation.
simulation_context.stop()
simulation_app.close()
