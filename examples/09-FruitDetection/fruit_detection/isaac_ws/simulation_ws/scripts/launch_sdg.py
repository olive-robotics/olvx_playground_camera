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

"""Generate a synthetic dataset."""

import argparse
import carb
from datetime import datetime
from isaacsim import SimulationApp
import numpy as np
import yaml


# Function to load the YAML configuration
def load_config(yaml_file_path):
    """
    Load the config yaml file.

    :param yaml_file_path: Path to yaml file.
    :return: A yaml object with the configuration.
    """
    try:
        with open(yaml_file_path, "r") as file:
            config = yaml.safe_load(file)
            return config
    except yaml.YAMLError as exc:
        print(f"Error while reading YAML file: {exc}")
        return None


# Keeps track of the frame index. It helps to switch the height level
# of each object. The sequence is: apple - avocado - lime. The function that
# moves the lime will also increment it.
frame_index = 0


def register_move_objects(config, rep):
    """
    Register objects in the scene.

    :param config: A yaml object with the configuration.
    :param rep: The omni.replicator.core module
    """

    def move_apple():
        global frame_index  # Ensure frame_index is shared across functions
        apple_z = config["OBJECTS_Z"][(frame_index + 0) % 3]
        APPLE_POSE_CONFIG = config["OBJECTS_POSE_CONFIG"]
        APPLE_POSE_CONFIG["min_pos"] = (
            APPLE_POSE_CONFIG["min_pos"][0],
            APPLE_POSE_CONFIG["min_pos"][1],
            apple_z,
        )
        APPLE_POSE_CONFIG["max_pos"] = (
            APPLE_POSE_CONFIG["max_pos"][0],
            APPLE_POSE_CONFIG["max_pos"][1],
            apple_z,
        )
        # Obtain the prim.
        object_prims = rep.get.prims(
            semantics=[("class", config["SEMANTIC_OBJECTS"]["Apple"]["class"])]
        )

        # Randomize the pose.
        with object_prims:
            rep.modify.pose(
                position=rep.distribution.uniform(
                    APPLE_POSE_CONFIG["min_pos"], APPLE_POSE_CONFIG["max_pos"]
                ),
                rotation=rep.distribution.uniform(
                    APPLE_POSE_CONFIG["min_rot"], APPLE_POSE_CONFIG["max_rot"]
                ),
            )
        return object_prims.node

    def move_avocado():
        global frame_index  # Ensure frame_index is shared across functions
        avocado_z = config["OBJECTS_Z"][(frame_index + 1) % 3]
        AVOCADO_POSE_CONFIG = config["OBJECTS_POSE_CONFIG"]
        AVOCADO_POSE_CONFIG["min_pos"] = (
            AVOCADO_POSE_CONFIG["min_pos"][0],
            AVOCADO_POSE_CONFIG["min_pos"][1],
            avocado_z,
        )
        AVOCADO_POSE_CONFIG["max_pos"] = (
            AVOCADO_POSE_CONFIG["max_pos"][0],
            AVOCADO_POSE_CONFIG["max_pos"][1],
            avocado_z,
        )

        # Obtain the prim.
        object_prims = rep.get.prims(
            semantics=[
                ("class", config["SEMANTIC_OBJECTS"]["Avocado"]["class"]),
            ]
        )

        # Randomize the pose.
        with object_prims:
            rep.modify.pose(
                position=rep.distribution.uniform(
                    AVOCADO_POSE_CONFIG["min_pos"],
                    AVOCADO_POSE_CONFIG["max_pos"],
                ),
                rotation=rep.distribution.uniform(
                    AVOCADO_POSE_CONFIG["min_rot"],
                    AVOCADO_POSE_CONFIG["max_rot"],
                ),
            )
        return object_prims.node

    def move_lime():
        global frame_index  # Ensure frame_index is shared across functions
        lime_z = config["OBJECTS_Z"][(frame_index + 2) % 3]
        frame_index += 1  # Increment frame_index for next cycle
        LIME_POSE_CONFIG = config["OBJECTS_POSE_CONFIG"]
        LIME_POSE_CONFIG["min_pos"] = (
            LIME_POSE_CONFIG["min_pos"][0],
            LIME_POSE_CONFIG["min_pos"][1],
            lime_z,
        )
        LIME_POSE_CONFIG["max_pos"] = (
            LIME_POSE_CONFIG["max_pos"][0],
            LIME_POSE_CONFIG["max_pos"][1],
            lime_z,
        )

        # Obtain the prim.
        object_prims = rep.get.prims(
            semantics=[("class", config["SEMANTIC_OBJECTS"]["Lime"]["class"])]
        )

        # Randomize the pose.
        with object_prims:
            rep.modify.pose(
                position=rep.distribution.uniform(
                    LIME_POSE_CONFIG["min_pos"], LIME_POSE_CONFIG["max_pos"]
                ),
                rotation=rep.distribution.uniform(
                    LIME_POSE_CONFIG["min_rot"], LIME_POSE_CONFIG["max_rot"]
                ),
            )
        return object_prims.node

    # Register the movement functions
    rep.randomizer.register(move_apple)
    rep.randomizer.register(move_avocado)
    rep.randomizer.register(move_lime)


def register_lights(config, rep):
    """
    Register lights in the scene.

    :param config: A yaml object with the configuration.
    :param rep: The omni.replicator.core module
    """

    def create_light_node(type: str):
        light = rep.create.light(
            light_type=type,
            color=rep.distribution.uniform(
                config["LIGHT_CONFIG"]["min_color"],
                config["LIGHT_CONFIG"]["max_color"],
            ),
            intensity=rep.distribution.uniform(
                config["LIGHT_CONFIG"][f"min_{type}_intensity"],
                config["LIGHT_CONFIG"][f"max_{type}_intensity"],
            ),
            position=rep.distribution.uniform(
                config["LIGHT_CONFIG"]["min_pos"],
                config["LIGHT_CONFIG"]["max_pos"],
            ),
            temperature=rep.distribution.uniform(
                config["LIGHT_CONFIG"]["min_temperature"],
                config["LIGHT_CONFIG"]["max_temperature"],
            ),
            exposure=rep.distribution.uniform(
                config["LIGHT_CONFIG"]["min_exposure"],
                config["LIGHT_CONFIG"]["max_exposure"],
            ),
            scale=1.0,
            count=1,
        )
        return light.node

    def randomize_distant_light():
        return create_light_node("distant")

    def randomize_cylinder_light():
        return create_light_node("cylinder")

    def randomize_sphere_light():
        return create_light_node("sphere")

    rep.randomizer.register(randomize_distant_light)
    rep.randomizer.register(randomize_cylinder_light)
    rep.randomizer.register(randomize_sphere_light)


def register_groundplane_colors(rep):
    """
    Register groundplane colors in the scene.

    :param rep: The omni.replicator.core module
    """

    def randomize_groundplane_colors():
        object_prims = rep.get.prims(path_pattern="/World/GroundPlane")
        with object_prims:
            rep.randomizer.color(
                colors=rep.distribution.uniform(
                    (0, 0, 0),
                    (1, 1, 1),
                )
            )
        return object_prims.node

    rep.randomizer.register(randomize_groundplane_colors)


def main(args):
    """Load a scene and generate a randomized dataset."""
    # Load the configuration file
    config = load_config(args.config_file)

    if config is None:
        print("Failed to load configuration file. Exiting.")
        return

    # Initialize SimulationApp
    stamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    if "{{ timestamp }}" in config["WRITER_CONFIG"]["output_dir"]:
        config["WRITER_CONFIG"]["output_dir"] = config["WRITER_CONFIG"][
            "output_dir"
        ].replace("{{ timestamp }}", stamp_str)

    simulation_app = SimulationApp(
        launch_config=config["SIMULATION_APP_CONFIG"],
    )

    # Import Replicator after SimulationApp is initialized
    import omni.replicator.core as rep
    from omni.isaac.core.physics_context import PhysicsContext
    from omni.isaac.core.objects.ground_plane import GroundPlane
    from omni.isaac.core.utils import prims
    from omni.isaac.core.utils.semantics import remove_all_semantics
    from omni.isaac.core.utils.stage import get_current_stage, create_new_stage
    from omni.isaac.nucleus import get_assets_root_path
    from pxr import Gf

    # Configure replicator settings
    rep.settings.carb_settings("/omni/replicator/RTSubframes", 3)

    # Get server path
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        carb.log_error(
            "Could not get nucleus server path, closing application.",
        )
        simulation_app.close()

    # Creates a new stage
    if not create_new_stage():
        carb.log_error(
            "Could not create a new stage, closing the application.",
        )
        simulation_app.close()
    stage = get_current_stage()

    # Disable capture on play (data generation will be triggered manually)
    rep.orchestrator.set_capture_on_play(False)

    # Clear any previous semantic data in the loaded stage
    for prim in stage.Traverse():
        remove_all_semantics(prim, False)

    # Create a ground plane
    PhysicsContext()
    GroundPlane(
        prim_path="/World/GroundPlane",
        size=10,
        color=np.array(
            [1.0, 1.0, 1.0],
        ),
    )

    # Spawn objects: Apple, Avocado and Lime in a random pose.
    prims.create_prim(
        prim_path=config["SEMANTIC_OBJECTS"]["Apple"]["prim"],
        position=(-0.1, -0.05, 0.5),
        orientation=(1.0, 0.0, 0.0, 0.0),
        scale=config["OBJECTS_SCALE"],
        usd_path=config["SEMANTIC_OBJECTS"]["Apple"]["url"],
        semantic_label=config["SEMANTIC_OBJECTS"]["Apple"]["class"],
    )

    prims.create_prim(
        prim_path=config["SEMANTIC_OBJECTS"]["Avocado"]["prim"],
        position=(0, 0.1, 0.5),
        orientation=(1.0, 0.0, 0.0, 0.0),
        scale=config["OBJECTS_SCALE"],
        usd_path=config["SEMANTIC_OBJECTS"]["Avocado"]["url"],
        semantic_label=config["SEMANTIC_OBJECTS"]["Avocado"]["class"],
    )

    prims.create_prim(
        prim_path=config["SEMANTIC_OBJECTS"]["Lime"]["prim"],
        position=(0.1, -0.05, 0.5),
        orientation=(1.0, 0.0, 0.0, 0.0),
        scale=config["OBJECTS_SCALE"],
        usd_path=config["SEMANTIC_OBJECTS"]["Lime"]["url"],
        semantic_label=config["SEMANTIC_OBJECTS"]["Lime"]["class"],
    )

    # Create the camera used for the acquisition
    sdg_camera = rep.create.camera(
        name=config["SDG_CAMERA"]["name"],
        position=config["SDG_CAMERA"]["pos"],
        rotation=config["SDG_CAMERA"]["rot"],
        focal_length=config["SDG_CAMERA"]["focal_length"],
        focus_distance=config["SDG_CAMERA"]["focus_distance"],
        f_stop=config["SDG_CAMERA"]["f_stop"],
        horizontal_aperture=config["SDG_CAMERA"]["horizontal_aperture"],
        clipping_range=Gf.Vec2f(*config["SDG_CAMERA"]["clipping_range"]),
        projection_type=config["SDG_CAMERA"]["projection_type"],
        count=1,
    )

    sdg_camera_render_product = rep.create.render_product(
        sdg_camera,
        (config["SDG_CAMERA"]["width"], config["SDG_CAMERA"]["height"]),
        name="SdgCameraView",
    )
    sdg_camera_render_product.hydra_texture.set_updates_enabled(False)

    # Register movement and light randomizations,
    # randomize colors, and attach writer
    register_move_objects(config, rep)
    register_lights(config, rep)
    register_groundplane_colors(rep)

    # Get writer and initialize with config
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(**config["WRITER_CONFIG"])

    # Attach writer to the render product
    writer.attach(sdg_camera_render_product)

    # Trigger randomization for every frame
    with rep.trigger.on_frame():
        rep.randomizer.randomize_distant_light()
        rep.randomizer.randomize_cylinder_light()
        rep.randomizer.randomize_sphere_light()
        rep.randomizer.move_apple()
        rep.randomizer.move_avocado()
        rep.randomizer.move_lime()
        rep.randomizer.randomize_groundplane_colors()

    sdg_camera_render_product.hydra_texture.set_updates_enabled(True)

    # Start the SDG
    print(f"Running SDG for {config['NUM_FRAMES']} frames")
    for i in range(config["NUM_FRAMES"]):
        rep.orchestrator.step(delta_time=0.0)

    # Cleanup writer and render products
    writer.detach()
    sdg_camera_render_product.destroy()

    # Wait for the data to be written to disk
    rep.orchestrator.wait_until_complete()

    while simulation_app.is_running():
        simulation_app.update()
    simulation_app.close()


# Argument parsing for command-line inputs
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load a YAML configuration file for the simulation."
    )
    parser.add_argument(
        "--config_file",
        type=str,
        default="/root/isaac_ws/simulation_ws/conf/config.yml",
        help="Path to the YAML configuration file \
            (default: /root/isaac_ws/simulation_ws/conf/config.yml)",
    )
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args)
