ARG ROS_DISTRO=humble

FROM osrf/ros:${ROS_DISTRO}-desktop-full AS detection_prod

ENV DEBIAN_FRONTEND=noninteractive

COPY --link detection_ws/src/fruit_detection/package.xml /root/detection_ws/src/fruit_detection/package.xml

WORKDIR /root/detection_ws/

RUN apt-get update && \
    apt-get install python3-pip -y && \
    rosdep update && \
    rosdep install --from-paths src -y --rosdistro=${ROS_DISTRO} && \
    rm -rf rm -rf /var/lib/apt/lists/*

COPY --link detection_ws /root/detection_ws/

RUN colcon build --event-handlers console_direct+

RUN echo "source /root/detection_ws//install/setup.bash" >> ~/.bashrc && \
    echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

ENTRYPOINT [ "/usr/bin/bash" ]

FROM detection_prod AS detection_test

WORKDIR /root/detection_ws/

SHELL ["/bin/bash", "-c"]

RUN source /root/detection_ws//install/setup.bash && \
    source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon test --event-handlers console_direct+
