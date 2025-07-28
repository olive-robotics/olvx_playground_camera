ARG ROS_DISTRO=humble

FROM osrf/ros:${ROS_DISTRO}-desktop-full

WORKDIR /root

RUN mkdir /root/rosbags/

# hadolint ignore=SC2086, DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip ros-${ROS_DISTRO}-rosbag2 && \
    rm -rf rm -rf /var/lib/apt/lists/*


ENTRYPOINT [ "/usr/bin/bash" ]
