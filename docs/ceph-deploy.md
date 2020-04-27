[Index](/)
\> [Installing Ceph](/ceph-install.html)
\> Deploying Ceph

# Deploying Ceph

Ceph is deployed using the [Ceph-Ansible project](https://github.com/ceph/ceph-ansible)
The Ansible playbooks and their dependencies have been bundled into Breqwatr's
[ceph-ansible image](https://hub.docker.com/r/breqwatr/ceph-ansible) and are
orchestrated by [bwdt](/installation.html)

Before you can deploy Ceph, ensure you have generated the required
[configuration files](/ceph-ansible-configs.html)

To show the deployment command's help text:

```bash
bwdt ceph ceph-ansible --help
```
To install Ceph:

```bash
bwdt ceph ceph-ansible \
  --inventory <path to inventory file> \
  --group-vars <path to group_vars directory> \
  --ssh-key <path to ssh private key file (usually id_rsa)>
```


## Double-check osd memory target

In the deployed servers hosting the OSD roles, check ceph.conf's
`osd memory target` value. Sometimes ceph-ansible picks a value that is WAY
too high. This is the ammount of ram **each** OSD service will use under high
load.
