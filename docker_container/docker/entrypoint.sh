#!/bin/bash

# NEST environment
source /opt/nest/bin/nest_vars.sh


cd /tmp
wget https://raw.githubusercontent.com/clinssen/OCNS-2020-workshop/master/materials/docker/jupyter_notebook_config.py
mkdir $HOME/.jupyter
cp jupyter_notebook_config.py $HOME/.jupyter/jupyter_notebook_config.py
cd



jupyter-lab &

# Start NEST Server
nest-server start -d -h 0.0.0.0 -u nest &

# Start NEST Desktop
nest-desktop start -h 0.0.0.0 &

/bin/bash

