# olimar

## Node Setup
awolf
awolf

### Install Docker
1. sudo apt update
2. sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
3. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
4. echo "deb [arch=arm64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
5. sudo apt update
6. apt-cache policy docker-ce
7. sudo apt-get install -y docker-ce docker-ce-cli containerd.io
8. 
8. sudo systemctl status docker
9. sudo systemctl edit docker.service

[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.soc>



10.  sudo systemctl daemon-reload
11.  sudo systemctl restart docker.service
12.  sudo netstat -lntp | grep dockerd
