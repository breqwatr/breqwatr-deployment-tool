[Index](/)
\> [Installing Ceph](/ceph-install.html)
\> Ceph Server Requirements

# Ceph Server Requirements


In general the requirements are as follows:


## Ubuntu & Ansible dependencies

Since Ceph is deployed with Ansible, the server needs to be configured such
that the deployment server has network connectivity to each Ceph server.

### Python

Python needs to be installed for Ansible to remotely operate the server:

```bash
apt-get install -y python
```

### SSH Key & Root access

The SSH service should allow root SSH access via private-key only, and have
the Ansible server's private key listed in its `/root/.ssh/authorized_keys`
file.



## Minimum Hardware Requirements

Minimal clusters are for POC, testing, and low-cost situations but generally
are not fit for production.

- Ubuntu 18.04
- One server hosting all Ceph services. For HA, 3 servers.
- One dedicated OSD drive, 2 if you want redundancy - separate from OS drive
- One 10GB/s or faster interface, 2 for HA
- 16GB RAM for an all-in-one deployment


## Suggested Hardware Requirements

There's a lot that goes into choosing the ideal hardware for Ceph. These are
only rough guidelines.

For more details, [check here](https://docs.ceph.com/docs/jewel/start/hardware-recommendations/)

- Ubuntu 18.04 on all nodes using Breqwatr's local Apt mirror for stability
- Single-socket servers with high clock speed
- 3+ Dedicated control plane servers separate from OSD servers
- All SSD storage drives for OSDs (data disks) - Lower latency the better
- More OSD servers with fewer disks are preferred over the opposite
- 32GB RAM (+ 1GB RAM per 1TB data storage on OSD nodes) - More is better
- Having 4 interfaces in 2 bonds allows isolating client traffic, which can
  improve security in some situations.
- MTU 9000 on interfaces and upstream switches



