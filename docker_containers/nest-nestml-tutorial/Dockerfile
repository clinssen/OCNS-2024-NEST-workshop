#FROM nestsim/nest:latest
FROM nest-simulator-dev

RUN apt-get update && apt-get install -y build-essential python3-dev python3-pip git nodejs curl cmake libboost-all-dev wget libncurses-dev libreadline-dev
#RUN apt-get remove -y python3-terminado
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install uwsgi jupyterlab scikit-learn tqdm --ignore-installed
RUN python3 -m pip install git+https://github.com/nest/ode-toolbox
#RUN python3 -m pip install nestml # XXX: we're using the latest master instead of the latest release!
#RUN python3 -m pip install nestml --pre
RUN python3 -m pip install git+https://github.com/clinssen/nestml@stdp-dopa-tutorial --upgrade

RUN cd && git clone https://github.com/clinssen/nestml && cd nestml && git checkout stdp-dopa-tutorial && cd

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
