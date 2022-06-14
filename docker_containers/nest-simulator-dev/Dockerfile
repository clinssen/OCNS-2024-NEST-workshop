FROM docker-registry.ebrains.eu/nest/nest-simulator:nest-simulator-build-base as builder
LABEL maintainer="s.graber@fz-juelich.de"

ARG NEST_VERSION=master
ARG SRC_PATH=/tmp

# Install NEST and NESTML
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
    make -j 8 && \
    make html && \
    make install



###############################################################################
# DEPLOY

FROM docker-registry.ebrains.eu/nest/nest-simulator:nest-simulator-deploy-base
LABEL maintainer="s.graber@fz-juelich.de"

COPY --from=builder /opt/nest /opt/nest
COPY --from=builder /opt/music-install /opt/music-install
