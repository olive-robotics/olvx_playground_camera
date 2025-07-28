ARG ROS_DISTRO=humble

FROM osrf/ros:${ROS_DISTRO}-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

ENTRYPOINT [ "/usr/bin/bash" ]
