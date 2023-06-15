#!/bin/bash

# NEST environment
source /opt/nest/bin/nest_vars.sh


cd /tmp
wget https://raw.githubusercontent.com/clinssen/OCNS-2023-NEST-workshop/master/docker_containers/nest-nestml-tutorial/jupyter_notebook_config.py
mkdir $HOME/.jupyter
cp jupyter_notebook_config.py $HOME/.jupyter/jupyter_notebook_config.py
cp jupyter_notebook_config.py $HOME/.jupyter/jupyter_lab_config.py
cd



jupyter-lab &

mv -f OCNS-2023-NEST-workshop /tmp/
git clone https://github.com/clinssen/OCNS-2023-NEST-workshop
cd OCNS-2023-NEST-workshop/materials
mv nestml /tmp/orig-workshop-NESTML-materials
git clone https://github.com/nest/nestml
cd ..

/bin/bash

