- APPLY FOR RESOURCES

	https://dispatch.fz-juelich.de:8817/kurs_login/back=/ABBRUCH

	Since we have 40 participants, you could ask for ~ 60,000 core-hours in total on the CPU.

	ie. 128 cores per compute node on JUSUF X 12 hours X 40 nodes ~= 60,000

	- JUSUF Compute nodes(HPC accounts) --> no internet access but more powerful
	- JSC Cloud --> On the cloud, there is no need to go through the JuDoor. There is a possibility to have a list of usernames and passwords in advance. Compute resources quite limited (RAM/CPU).


- JOIN TRAINING PROJECT

	https://judoor.fz-juelich.de/login

	enter the training2422 project. Make sure it shows up under "JUSUF_CPU".


- LAUNCH THE SERVER

	https://jupyter.jsc.fz-juelich.de
	(log into own account)

	new ->
		JupyterLab 4.2
		JUSUF
		linssen1
		use the training2422 project


- CREATE CUSTOM KERNEL

	First, compile NEST.

	Use the same modules as in the custom kernel build script. Also do a 

		ml Boost/1.82.0

	Clone and build:

		mkdir /p/project1/training2422/linssen1/nest
		cd /p/project1/training2422/linssen1/nest
		git clone https://github.com/nest/nest-simulator
		mkdir /p/project1/training2422/linssen1/nest/nest-simulator-build
		cd /p/project1/training2422/linssen1/nest/nest-simulator-build
		cmake -DCMAKE_INSTALL_PREFIX:PATH=../nest-simulator-install ../nest-simulator
		make -j32 install

	See https://github.com/FZJ-JSC/jupyter-jsc-notebooks/tree/documentation/03-HowTos for Sandra's script creating a custom kernel.

	delete the old kernel:

		rm -rv /p/project1/training2422/linssen1/jupyter/kernels/ocns_2024_nest_nestml_kernel
		rm -rv /p/project1/training2422/.local/share/jupyter/kernels/ocns_2024_nest_nestml_kernel

	> I have used this one in the past: https://github.com/FZJ-JSC/jupyter-jsc-notebooks/blob/documentation/03-HowTos/Create_JupyterKernel_general.ipynb

	> The example that I implemented, which might be a bit outdated, is here: https://gitlab.jsc.fz-juelich.de/metaopt/freiburg2023/-/blob/main/create_kernel.sh

	> The user just needs to do ./create_kernel.sh from the command line the first time from their home directory, then all is configured. Just a quick note on this script, I made a shared installation of nest in a specific path, I specify this in the script for the kernel in lines 106 and 107 where I say:

		export PYTHONPATH=$PYTHONPATH:/p/project/training2222/nest-simulator/build/install/lib64/python3.9/site-packages:/p/project/training2222/L2L/:/p/project/training2222/sdict/:/p/project/training2222/JUBE/:/p/project/training2222/JUBE/bin/
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/p/project/training2222/JUBE/bin/

	you can do a similar thing for nest and nestml.


	$ echo $PROJECT
	/p/project1/training2422

	Edit the script and give the kernel a name and set type to project. Add custom pip install commands, etc. Then run:

	$ ./create_custom_kernel_sandra.sh

	In my case it printed something like:

	jupyter search paths for kernels-directories
	/p/project1/training2422/.local/share/jupyter
	project kernel
	/p/project1/training2422/.local/share/jupyter/kernels/ocns_2024_nest_nestml_kernel

	...

	The new kernel 'ocns_2024_nest_nestml_kernel' was added to your kernels in '/p/project1/training2422/.local/share/jupyter/kernels/'


- POST KERNEL SETUP STEPS

	Run the following code in a new notebook under your own account name:

		import neat
		import neatmodels
		import nest
		neatmodels.load_or_install_neuron_bbp_channels()
		neatmodels.load_or_install_nest_bbp_channels()



- DISTRIBUTE CUSTOM KERNEL

	You could place the kernel in $PROJECT/.local  (in the same way as it would be in $HOME/.local) and makes it readable to every project member so that everyone will see your kernel right away

	Check for a list of kernels:

		ls -l $PROJECT/.local/share/jupyter/kernels


- INVITE STUDENTS

	for the instructions sheet: https://clinssen.github.io/OCNS-2024-NEST-workshop/

	for the invite link, see JuDoor

	e.g. of the form: https://judoor.fz-juelich.de/projects/join/training2422

