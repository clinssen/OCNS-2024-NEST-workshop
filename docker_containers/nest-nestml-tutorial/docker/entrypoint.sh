#!/bin/bash

# NEST environment
source /opt/nest/bin/nest_vars.sh


cd /tmp
wget https://raw.githubusercontent.com/clinssen/OCNS-2020-workshop/master/materials/docker/nest-nestml-tutorial/jupyter_notebook_config.py
mkdir $HOME/.jupyter
cp jupyter_notebook_config.py $HOME/.jupyter/jupyter_notebook_config.py
cd



jupyter-lab &

git clone https://github.com/clinssen/OCNS-2020-workshop

/bin/bash

