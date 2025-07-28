"""Set up the fruit detection node."""

import os
from glob import glob

from setuptools import find_packages, setup

PACKAGE_NAME = "fruit_detection"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + PACKAGE_NAME],
        ),
        ("share/" + PACKAGE_NAME, ["package.xml"]),
        (
            os.path.join("share", PACKAGE_NAME, "config"),
            glob(os.path.join("config", "*")),
        ),
        (
            os.path.join("share", PACKAGE_NAME, "launch"),
            glob(os.path.join("launch", "*launch.py")),
        ),
    ],
    install_requires=["setuptools", "torch", "torchvision"],
    zip_safe=True,
    maintainer="Agustin Alba Chicar",
    maintainer_email="ag.albachicar@ekumenlabs.com",
    description="Creates a detection in the camera feed.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "fruit_detection_node = fruit_detection.fruit_detection_node:main",
        ],
    },
)
