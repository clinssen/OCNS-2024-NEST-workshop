#cloud-config
runcmd:
- apt remove docker docker-engine docker.io containerd runc
- apt update
- apt install -y ca-certificates curl gnupg lsb-release
- mkdir -m 0755 -p /etc/apt/keyrings
- curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
- echo \
  "deb [trusted=yes arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
- chmod a+r /etc/apt/keyrings/docker.gpg
- apt-get update
- apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
- apt install -y python3-wheel 
- apt install -y docker-compose
- curl https://raw.githubusercontent.com/clinssen/HBP-summit-2023-workshop/master/docker_containers/nest-nestml-tutorial/etc_docker_daemon.json -o /etc/docker/daemon.json
- systemctl start docker
- usermod -aG docker ubuntu
- su -c "curl https://raw.githubusercontent.com/clinssen/HBP-summit-2023-workshop/master/docker_containers/docker-compose.yml -o /home/ubuntu/docker-compose.yml" - ubuntu
- su -c "docker pull clifzju/nest-nestml-jupyterlab-ocns-tutorial" - ubuntu
- su -c "docker run -i -d -p 7003:7003 -t clifzju/nest-nestml-jupyterlab-ocns-tutorial" - ubuntu
- su -c "cd && docker-compose up -d" - ubuntu
