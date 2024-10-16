# INPUT NEEDED:
KERNEL_NAME=ocns_2024_nest_nestml_kernel

export KERNEL_NAME=$(echo "${KERNEL_NAME}" | awk '{print tolower($0)}')
echo ${KERNEL_NAME} # double check

# JUPYTER SEARCH PATH (for kernels-directory)
echo "jupyter search paths for kernels-directories"
if [ -z $JUPYTER_PATH ]; then
  echo "$HOME/.local/share/jupyter"
else
  tr ':' '\n' <<< "$JUPYTER_PATH"
fi

# INPUT NEEDED:
export KERNEL_TYPE=project # private, project or other
export KERNEL_SPECS_PREFIX=${HOME}/.local

###################
# project kernel
if [ "${KERNEL_TYPE}" == "project" ]; then
  export KERNEL_SPECS_PREFIX=${PROJECT}/.local
  echo "project kernel"
# private kernel
elif [ "${KERNEL_TYPE}" == "private" ]; then
  export KERNEL_SPECS_PREFIX=${HOME}/.local
  echo "private kernel"
else
  if [ ! -d "$KERNEL_SPECS_PREFIX" ]; then
    echo "ERROR: please create directory $KERNEL_SPECS_PREFIX"
  fi
  echo "other kernel"
fi
export KERNEL_SPECS_DIR=${KERNEL_SPECS_PREFIX}/share/jupyter/kernels

# check if kernel name is unique
if [ -d "${KERNEL_SPECS_DIR}/${KERNEL_NAME}" ]; then
  echo "ERROR: Kernel already exists in ${KERNEL_SPECS_DIR}/${KERNEL_NAME}"
  echo "       Rename kernel name or remove directory."
fi

echo ${KERNEL_SPECS_DIR}/${KERNEL_NAME} # double check

# INPUT NEEDED:
export KERNEL_VENVS_DIR=${PROJECT}/${USER}/jupyter/kernels

###################
mkdir -p ${KERNEL_VENVS_DIR}
if [ "${KERNEL_TYPE}" != "private" ] && [ "${KERNEL_TYPE}" != "other" ]; then
  echo "Please check the permissions and ensure your project partners have read/execute permissions:"
  namei -l ${KERNEL_VENVS_DIR}
fi

echo ${KERNEL_VENVS_DIR} # double check
ls -lt ${KERNEL_VENVS_DIR}

module -q purge
module -q use $OTHERSTAGES
# XXX: was /2022 originally!
module -q load Stages/2024
module -q load GCCcore/.12.3.0
module -q load GCC
module -q load ParaStationMPI
module -q load CMake
# XXX: was without a version originally
module -q load Python
module -q load SciPy-Stack
module -q load GSL
module -q load mpi4py
if [ -d "${KERNEL_VENVS_DIR}/${KERNEL_NAME}" ]; then
  echo "ERROR: Directory for virtual environment already ${KERNEL_VENVS_DIR}/${KERNEL_NAME}"
  echo "       Rename kernel name or remove directory."
else
  python -m venv --system-site-packages ${KERNEL_VENVS_DIR}/${KERNEL_NAME}
  source ${KERNEL_VENVS_DIR}/${KERNEL_NAME}/bin/activate
  export PYTHONPATH=/p/project1/training2422/linssen1/site-packages:${VIRTUAL_ENV}/lib/python3.11/site-packages:${PYTHONPATH}
  echo "Virtual environment initialized to: "
  echo ${VIRTUAL_ENV} # double check
fi

which pip
if [ -z "${VIRTUAL_ENV}" ]; then
  echo "ERROR: Virtual environment not successfully initialized."
else
  pip install --prefix ${VIRTUAL_ENV} --ignore-installed ipykernel
  ls ${VIRTUAL_ENV}/lib/python3.11/site-packages/ # double check
fi

# --prefix /p/project1/training2422/linssen1/site-packages
pip install --prefix ${VIRTUAL_ENV} scikit-learn
pip install --prefix ${VIRTUAL_ENV} tqdm
pip install --prefix ${VIRTUAL_ENV} git+https://github.com/nest/ode-toolbox
pip install --prefix ${VIRTUAL_ENV} PyNN
# parameters package is needed for the sequence learning tutorial!
pip install --prefix ${VIRTUAL_ENV} parameters jupytext
# pip install --user neatdend

pip install --prefix ${VIRTUAL_ENV} git+https://github.com/clinssen/nestml@sequence_learning_and_compartmental_vectorization

pip install --prefix ${VIRTUAL_ENV} git+https://github.com/WillemWybo/NEAT-2@enh/nestml-channel-generation
pip install --prefix ${VIRTUAL_ENV} /p/project1/training2422/linssen1/NEATmodels-master-2024-07-15.zip

#cd nestml
#python setup.py install

echo '#!/bin/bash'"

# Load basic Python module
module -q purge
module -q use $OTHERSTAGES        
module -q load Stages/2024
module -q load GCCcore/.12.3.0
module -q load GCC
module -q load ParaStationMPI
module -q load CMake
module -q load Python
module -q load SciPy-Stack
module -q load GSL
module -q load mpi4py
export PYTHONPATH=$PYTHONPATH:/p/project1/training2422/linssen1/site-packages:/p/project1/training2422/linssen1/nest/nest-simulator-install/lib64/python3.11/site-packages
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/p/project1/training2422/linssen1/nest/nest-simulator-install/lib64/nest

# Load extra modules you need for your kernel (as you did in step 1.2)
#module load <module you need>
    
# Activate your Python virtual environment
source ${KERNEL_VENVS_DIR}/${KERNEL_NAME}/bin/activate
    
# Ensure python packages installed in the virtual environment are always prefered
export PYTHONPATH=/p/project1/training2422/linssen1/site-packages:${VIRTUAL_ENV}/lib/python3.11/site-packages:"'${PYTHONPATH}'"

exec python -m ipykernel "'$@' > ${VIRTUAL_ENV}/kernel.sh
chmod +x ${VIRTUAL_ENV}/kernel.sh

cat ${VIRTUAL_ENV}/kernel.sh # double check

python -m ipykernel install --name=${KERNEL_NAME} --prefix ${VIRTUAL_ENV}
export VIRTUAL_ENV_KERNELS=${VIRTUAL_ENV}/share/jupyter/kernels

mv ${VIRTUAL_ENV_KERNELS}/${KERNEL_NAME}/kernel.json ${VIRTUAL_ENV_KERNELS}/${KERNEL_NAME}/kernel.json.orig

echo '{
  "argv": [
    "'${KERNEL_VENVS_DIR}/${KERNEL_NAME}/kernel.sh'",
    "-m",
    "ipykernel_launcher",
    "-f",
    "{connection_file}"
  ],
  "display_name": "'${KERNEL_NAME}'",
  "language": "python"
}' > ${VIRTUAL_ENV_KERNELS}/${KERNEL_NAME}/kernel.json

cat ${VIRTUAL_ENV_KERNELS}/${KERNEL_NAME}/kernel.json # double check

mkdir -p ${KERNEL_SPECS_DIR}
cd ${KERNEL_SPECS_DIR}
echo ${VIRTUAL_ENV_KERNELS}/${KERNEL_NAME}
ln -s ${VIRTUAL_ENV_KERNELS}/${KERNEL_NAME} .

echo -e "\n\nThe new kernel '${KERNEL_NAME}' was added to your kernels in '${KERNEL_SPECS_DIR}/'\n"
ls ${KERNEL_SPECS_DIR} # double check

deactivate
