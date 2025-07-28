ARG ROS_DISTRO=humble

FROM osrf/ros:${ROS_DISTRO}-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y --no-install-recommends ros-${ROS_DISTRO}-usb-cam && \
    rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc

COPY --link docker/camera_params.yml /root/camera_params.yml

CMD [ "/usr/bin/bash", "-c", "ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /root/camera_params.yml" ]
