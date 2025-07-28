ARG ISAAC_SIM_VERSION=4.1.0

FROM nvcr.io/nvidia/isaac-sim:${ISAAC_SIM_VERSION}

ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && \
    apt install --no-install-recommends -y \
        apt-utils \
        bash-completion \
        curl \
        locales \
        lsb-release \
        python3 \
        python3-pip \
        python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root/isaac_ws

CMD [ "/usr/bin/bash" ]
