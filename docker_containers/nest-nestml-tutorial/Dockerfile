# FROM buildpack-deps:focal as builder
FROM ubuntu:22.04
LABEL maintainer="s.graber@fz-juelich.de"

ENV TERM=xterm \
    TZ=Europe/Berlin \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    automake \
    autotools-dev \
    build-essential \
    ccache \
    cmake \
    curl \
    cython3 \
    freeglut3-dev \
    git \
    gosu \
    jq \
    junitparser \
    less \
    libboost-filesystem-dev libboost-regex-dev libboost-wave-dev \
    libboost-python-dev libboost-program-options-dev libboost-test-dev \
    libboost-dev \
    libgomp1 \
    libgsl-dev  \
    libgsl0-dev \
    libhdf5-dev \
    libltdl-dev \
    libltdl7 \
    libmusic1v5 \
    libncurses-dev \
    libomp-dev \
    libopenmpi-dev \
    libpcre3 \
    libpcre3-dev \
    libpython3.10 \
    libreadline-dev \
    libreadline8 \
    libtool \
    libzmq3-dev \
    llvm-dev \
    nano \
    openmpi-bin \
    openssh-client \
    openssh-server \
    pandoc \
    pep8 \
    pkg-config \
    python3-dev \
    python3-flask \
    python3-flask-cors \
    python3-h5py \
    python3-ipython \
    python3-junitparser \
    python3-jupyter-core \
    python3-mpi4py \
    python3-nose \
    python3-pandas \
    python3-path \
    python3-pip \
    python3-pytest \
    python3-pytest-timeout \
    python3-pytest-xdist \
    python3-restrictedpython \
    python3-scipy \
    python3-setuptools \
    python3-sphinx \
    python3-statsmodels \
    python3-sympy \
    python3-tk \
    python3-tqdm \
    tcl8.6 \
    tcl8.6-dev \
    tk8.6-dev \
    uwsgi \
    vera++ \
    wget
    # update-alternatives --remove-all python && \
    #update-alternatives --install /usr/bin/python python /usr/bin/python3 10 && \
    #update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

RUN python3 -m pip install --upgrade pip setuptools wheel mock pandas numpy

ARG NEST_VERSION=master
ARG SRC_PATH=/tmp

RUN python3 -m pip install setuptools==68


# Install NEST
RUN wget https://github.com/nest/nest-simulator/archive/refs/heads/${NEST_VERSION}.tar.gz -P ${SRC_PATH} && \
    cd ${SRC_PATH} && tar -xzf ${NEST_VERSION}.tar.gz && ls -l && \
    python3 -m pip install -r ${SRC_PATH}/nest-simulator-${NEST_VERSION}/doc/requirements.txt   

RUN mkdir nest-build && cd nest-build && \
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/nest \
          -Dwith-warning=ON \
          -Dwith-boost=ON \
          -Dwith-ltdl=ON \
          -Dwith-gsl=ON \
          -Dwith-readline=ON \
          -Dwith-python=ON \
          -Dwith-mpi=ON \
          -Dwith-openmp=ON \
          -Dwith-libneurosim=OFF \
          -Dwith-music=/opt/music-install \
          ${SRC_PATH}/nest-simulator-${NEST_VERSION} && \
make -j8 && \
make install

# add user 'nest'
RUN adduser --disabled-login --gecos 'NEST' --home /home/nest nest && \
    chown nest:nest /home/nest

RUN apt-get update && apt-get install -y build-essential python3-dev python3-pip git nodejs curl cmake libboost-all-dev wget libncurses-dev libreadline-dev swig libgsl-dev
#RUN apt-get remove -y python3-terminado
RUN python3 -m pip install --upgrade pip setuptools wheel

RUN apt-get install -y --no-install-recommends libopenblas-dev

RUN python3 -m pip install git+https://github.com/pygsl/pygsl/
RUN python3 -m pip install uwsgi jupyterlab scikit-learn tqdm --ignore-installed
#RUN python3 -m pip install git+https://github.com/nest/ode-toolbox
RUN python3 -m pip install odetoolbox


# packages used specifically for tutorial material:
RUN python3 -m pip install seaborn

RUN python3 -m pip install h5py --upgrade

#RUN python3 -m pip install nestml # latest release
#RUN python3 -m pip install nestml --pre  # latest pre-release
#RUN python3 -m pip install git+https://github.com/clinssen/nestml@stdp-dopa-tutorial --upgrade   # latest from github
# RUN cd && git clone https://github.com/clinssen/nestml && cd nestml && git checkout stdp-dopa-tutorial && cd
#RUN git clone https://github.com/clinssen/nestml && cd nestml && git branch -a && git checkout stdp-dopa-tutorial-upstream && python3 setup.py install
#RUN python3 -m pip install git+https://github.com/clinssen/nestml@stdp-dopa-tutorial-upstream --upgrade
RUN python3 -m pip install git+https://github.com/clinssen/nestml@ebrains_day --upgrade

# copy entrypoint to nest home folder
COPY ./docker/entrypoint.sh /home/nest
RUN chown nest:nest /home/nest/entrypoint.sh && \
    chmod +x /home/nest/entrypoint.sh && \
    echo '. /opt/nest/bin/nest_vars.sh' >> /home/nest/.bashrc

COPY package.json /tmp/

# install nest-desktop and nest-server
#COPY ./nest-server.json /usr/local/lib/python3.6/dist-packages/nest_desktop/app/assets/config/nest-server/

#COPY ../../materials/nestml/*.ipynb /home/nest

#RUN python3 -m pip uninstall --yes antlr4-python3-runtime
#RUN yes | python3 -m pip install antlr4-python3-runtime==4.7.1

RUN chown -R nest:nest /opt/nest

#RUN cd nest-desktop
#RUN yarn build
#RUN cd ..

EXPOSE 7003
WORKDIR /home/nest
USER nest
ENTRYPOINT ["/home/nest/entrypoint.sh"]
