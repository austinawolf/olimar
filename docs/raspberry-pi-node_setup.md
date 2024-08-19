## Current Config

* Master Node: raspberrypi2, 192.168.0.250
* Worker Node: olimar-node, 192.168.0.173


## Raspberry Pi Setup

* Open Raspberry Pi Imager (Tested on v1.8.5)
* Setting:
* Raspberry Pi 4
* Ubuntu Server 22.04.4 LTS (64 Bit)
* username/password awolf/awolf

## PiMaster Setup (via ssh)

### Setup K3s master
* Install k3s: `curl -sfL https://get.k3s.io | sh -`
* Check status: `sudo systemctl status k3s`
* Update permissions for config: `sudo chmod 644 /etc/rancher/k3s/k3s.yaml`
* Get node token: `sudo cat /var/lib/rancher/k3s/server/node-token`
Example: `K10405b449ebbde21b43467bd84d9922c25b617f7e4e0e484a91708e0d8e222b3cf::server:55188d3c18a9f5ddd28d869c6b8b0a65`

### Setup docker registry
* Run `curl -fsSL https://get.docker.com -o get-docker.sh`
* Run `sudo sh get-docker.sh`
* Run `sudo usermod -aG docker $USER`
* Logout, then Login
* Run `docker run -d -p 5000:5000 --restart=always --name registry registry:2`
* Verify registry container is running `docker ps`

#### Pushing Example Image to Master Registry
* 
* docker tag example-env 192.168.0.250:5000/example-env
* docker push 192.168.0.250:5000/example-env

## Node Setup (via ssh)
* Need just the first section before the "::"
* `curl -sfL https://get.k3s.io | K3S_URL=https://192.168.0.250:6443 K3S_TOKEN=K10405b449ebbde21b43467bd84d9922c25b617f7e4e0e484a91708e0d8e222b3cf::server:55188d3c18a9f5ddd28d869c6b8b0a65 sh -`

#### Test Pull
* docker pull 192.168.0.250:5000/example-env

