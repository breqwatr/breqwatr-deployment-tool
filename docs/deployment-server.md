# Deployment Server

To deploy the cloud software, a stand-alone system outside the cloud is
required. We refer to this server as the "deployment server".

The deployment server is usually a VM on VMWare/HyperV or a very small physical
server deployed on an Intel Nuc or 1U rack-mount server. It typically runs
Ubuntu Server.

All of the usual auxiliary infrastructure expected to be ran "beside" the
private cloud clusters can be launched on this deployment server.


## Requirements

The following system requirements apply to the server used for deployments:

- Ubuntu 18.04 Bionic
- Python 3
- Docker
- 8GB RAM
- 60GB Disk
    - Less space can work, but increasing the volume used for Docker images can
      be troublesome so it's best to provision some extra space.
- Layer 3 network connectivity too all cloud servers for most services
- Layer 2 network connectivity for PXE


### Networking

For services such as Apt, Pip, and the local Docker registry, any routed Layer
3 network connectivity between the cloud servers and the deployment server is
sufficient.

If the deployment server will be used to PXE the metal cloud servers then it
needs to have one interface on the same VLAN and subnet as the cloud servers.

When installing OpenStack, we suggest that the deployment server holds an IP
address on the private/internal network.

When installing Ceph, the deployment server must have layer 3 connectivity with
the Ceph monitors nodes.


## Installing Required Software (Online)

When the deployment server has an outbound internet connection (it can ping
Google, for instance) it's trivial to install the required dependency software.

### Python3

```bash
apt-get update
apt-get install -y python3 python3-setuptools python3-pip
```

### Docker

```bash
apt-get update
apt-get install -y\
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
```
