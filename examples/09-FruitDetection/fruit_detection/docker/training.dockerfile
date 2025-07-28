FROM ubuntu:22.04 AS training_prod

WORKDIR /root/training_ws/
RUN mkdir data model model/out

RUN apt-get update && \
    apt-get install -y python3.10 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY --link training_ws/requirements.txt /root/training_ws/

RUN python3 -m pip install -r requirements.txt

COPY --link training_ws/ /root/training_ws/

ENTRYPOINT [ "/usr/bin/bash" ]
