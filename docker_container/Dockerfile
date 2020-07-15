FROM nestsim/nest:2.20.0
LABEL maintainer="Sebastian Spreizer <spreizer@web.de>"

RUN apt-get update && apt-get install -y build-essential python3-dev python3-pip git nodejs curl
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install uwsgi jupyterlab scikit-learn nestml

# add user 'nest'
RUN adduser --disabled-login --gecos 'NEST' --home /home/nest nest && \
    chown nest:nest /home/nest

# copy entrypoint to nest home folder
COPY ./docker/entrypoint.sh /home/nest
RUN chown nest:nest /home/nest/entrypoint.sh && \
    chmod +x /home/nest/entrypoint.sh && \
    echo '. /opt/nest/bin/nest_vars.sh' >> /home/nest/.bashrc

COPY package.json /tmp/

# install nest-desktop and nest-server
RUN export LC_CTYPE=C.UTF-8 && \
    python3 -m pip install nest-desktop==2.4.*
COPY ./nest-server.json /usr/local/lib/python3.6/dist-packages/nest_desktop/app/assets/config/nest-server/

EXPOSE 5000 8000 7003
WORKDIR /home/nest
USER nest
ENTRYPOINT ["/home/nest/entrypoint.sh"]

