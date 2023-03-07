#cloud-config
runcmd:
- yum install -y yum-utils dnf screen
- yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
- dnf install -y https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.6-3.3.el7.x86_64.rpm
- yum install -y python3-wheel docker-ce docker-ce-cli containerd.io epel-release
- yum install -y docker-compose
- mkdir /etc/docker
- curl https://raw.githubusercontent.com/clinssen/HBP-summit-2023-workshop/master/docker_containers/nest-nestml-tutorial/etc_docker_daemon.json -o /etc/docker/daemon.json
- systemctl start docker
- usermod -aG docker centos
- su -c "curl https://raw.githubusercontent.com/clinssen/HBP-summit-2023-workshop/master/docker_containers/docker-compose.yml -o /home/centos/docker-compose.yml" - centos
- su -c "docker pull clifzju/nest-nestml-jupyterlab-ocns-tutorial" - centos
- su -c "docker run -i -d -p 7003:7003 -t clifzju/nest-nestml-jupyterlab-ocns-tutorial" - centos
- su -c "cd && docker-compose up -d" - centos
