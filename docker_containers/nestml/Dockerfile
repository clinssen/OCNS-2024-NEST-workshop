FROM nest-simulator-custom
#FROM nestsim/nest:latest

RUN apt-get update && apt-get install -y build-essential python3-dev python3-pip git curl cmake libboost-all-dev wget
RUN python3 -m pip install --upgrade pip setuptools wheel

RUN pip install wheel
RUN pip install nestml

RUN /bin/bash

