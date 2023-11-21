Deploying NEST tutorial virtual machines
========================================

Deployment is done completely via Docker containers. NEST Desktop was deployed via its official Docker-compose mechanism, which internally uses one container for NEST-server and one for the graphical interface (also a web server). A separate Docker image was used to run the JupyterHub server for the NEST/NESTML scripts.


Configuration via web interface
-------------------------------

First, set up the basic configuration via the OpenStack web GUI.

https://cloud.jsc.fz-juelich.de/ (log in with LDAP credentials)

For instructions on network setup, see: https://apps.fz-juelich.de/jsc/hps/jusuf/index.html

Set up Jupyter notebook
-----------------------

Generate a password hash:

.. code-block:: sh

   python3 -c "from notebook.auth import passwd; passwd()"
   password = "hellocns2020"

Yields ``sha1:7a12c3c3439a:d74662fead39f17cabd747faf34a65bd58d135d3``. Copy this into ``jupyter_notebook_config.py``.


Building JupyterHub Docker image
--------------------------------

.. code-block:: sh

   docker login -u clifzju
   docker build -t nest-nestml-jupyterlab-ocns-tutorial . --no-cache
   docker tag nest-nestml-jupyterlab-ocns-tutorial clifzju/nest-nestml-jupyterlab-ocns-tutorial
   docker push clifzju/nest-nestml-jupyterlab-ocns-tutorial

Local test run:

.. code-block:: sh

   docker run XXX && docker logs $(docker ps -lq) -f
   docker run -it XXX /bin/bash

Options:

.. code-block:: sh

   --rm: auto remove container on exit
   -t: allocate pseudo TTY
   -i: keep stdin open even if not attached
   -p: port forwarding, e.g. -p 8443:443

Attach shell to a running container:

.. code-block:: sh

   docker exec -i -t f5fc06bbd63e /bin/bash

Forward directory X on host to Y in container:

.. code-block:: sh

   -v X:Y

Run as root? Add ``-u root``

Launching the VMs
-----------------

Use CentOS 7 image. Use cloud-init to launch the startup script when the instance boots.

For documentation, see:

- https://cloudinit.readthedocs.io/en/latest/topics/examples.html
- https://raymii.org/s/tutorials/Automating_Openstack_with_Cloud_init_run_a_script_on_VMs_first_boot.html

Debugging logs: see

- ``/var/log/boot.log``
- ``/var/log/cloud-init.log``
- ``/var/log/cloud-init-output.log``
- ``cloud-init analyze show -i my-cloud-init.log``

Some useful commands:

.. code-block:: sh

   openstack flavor list
   openstack image list
   openstack network list
   openstack security group list
   openstack floating ip list

Example for launching a single instance:

.. code-block:: sh

   openstack server create --image "CentOS-7-x86_64-GenericCloud-2003" --nic net-id="21196f6f-f1f5-4999-a040-51a0063eb250" --flavor "76f35bd5-4a7a-4b02-acf7-9add47dc659a" --user-data cloud_init.sh --security-group ssh-external --security-group http7000 --key-name nesttest INSTANCE_NAME
   
Example for allocating a single floating IP:

.. code-block:: sh

   openstack network list 

Returns e.g.:

::

   +--------------------------------------+---------------------+--------------------------------------+ 
   | ID                                   | Name                | Subnets                              | 
   +--------------------------------------+---------------------+--------------------------------------+ 
   | 21196f6f-f1f5-4999-a040-51a0063eb250 | jusuf-cloud-network | b0965bea-a818-4290-bee1-eee246921253 | 
   | adc8872c-1b9e-4e07-bef9-c316d586d281 | dmz-jusuf-cloud     | b0fd238a-6470-4389-a132-903ab74c7acb | 
   +--------------------------------------+---------------------+--------------------------------------+

Note the ID ``adc8872c-1b9e-4e07-bef9-c316d586d281``.

Then:

.. code-block:: sh

   openstack floating ip create adc8872c-1b9e-4e07-bef9-c316d586d281

Associate using:

.. code-block:: sh

   openstack server add floating ip INSTANCE_NAME 134.94.88.51

It is possible to log in via SSH using:

.. code-block:: sh

   ssh centos@134.94.88.xxx

Documentation links:

- https://apps.fz-juelich.de/jsc/hps/jusuf/cloud/access_cloud.html#access-cloud
- https://docs.openstack.org/mitaka/user-guide/sdk.html
- https://docs.openstack.org/mitaka/user-guide/sdk_compute_apis.html#create-server-api-v2

Apache reverse proxy
--------------------

.. note::

   Work in progress.

Let's say 192.168.0.128 is serving http on port 80. It has no public IP, and we want to use our server at 192.168.0.104, with public IP 134.94.88.51, to make it accessible via http://134.94.88.51:7010. Open the necessary TCP ports in the Openstack control panel (security groups), in this example 7010.

In ``/etc/httpd/conf/httpd.conf``:

.. code-block:: sh

   Listen 80 
   Listen 7010

Create a new file ``/etc/httpd/conf.d/vhosts.conf``:

::

   <VirtualHost *:7010> 
    ServerName 134.94.88.51 

    ProxyPass "/" "http://192.168.0.128:80/" 
    ProxyPassReverse "/" "http://192.168.0.128:80/" 
   </VirtualHost>

Update SELinux rules:

.. code-block:: sh

   sudo /usr/sbin/setsebool -P httpd_can_network_connect 1
   sudo semanage port --add 7010 --proto tcp --type http_port_t
   # sudo semanage port -l  | grep http

Restart apache:

.. code-block:: sh

   sudo systemctl restart httpd

