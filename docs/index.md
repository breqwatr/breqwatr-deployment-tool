# Breqwatr Deployment Tool

A command-line driven deployment toolkit for containerized, open source cloud
services such as OpenStack and Ceph. BWDT supports other useful containerized
services which enable air-gap/dark-site installations such as private Apt and
Pip repositories.

The Breqwatr Deployment Tool (BWDT) enables an offline, reliable, and easy
installation procedure for what are otherwise highly complicated tools. The
services deployed by BWDT are tested, stable, and intended for long-term
support.

With the exception of a few value-add services, namely Arcus and Support, all
Breqwatr tools are free and open source. You can use BWDT to deploy OpenStack
and Ceph in your environment without purchasing a license, though the images
will come from Docker Hub instead of Breqwatr's registry and might be a bit
older.



## Documentation

The Breqwatr Deployment Tool is used to deploy and manage all of the software
we support. It's freely available and simple to install.

[BWDT Installation & Requirements](/installation.html)


### Deployment Server

We suggest you dedicate a server to deploying the Breqwatr-supported services.
This server can also run the local mirrors to improve deployment speed and
software stability.

- [Creating Offline Installation Media](/offline-media.html)
- [Deployment Server](/deployment-server.html)
    - [Local Apt Service](/apt.html)
    - [Local Pip Service](/pip.html)
    - [Local Docker Registry](/registry.html)


### Ceph

For open-source cloud storage, Breqwatr recommends & supports [Ceph](https://ceph.io/).

- [Prepare Ceph Storage Servers](/ceph-server-setup.html)
- [Create Ceph-Ansible Configuration Files](/ceph-ansible-configs.html)
- [Deploy Ceph](ceph-deploy.html)
- Preparing Ceph for OpenStack
    - [Create Ceph's OSD Pools for OpenStack](/ceph-pools.html)
    - [Create CephX Authentication Keys](/ceph-cephx-keys.html)


### OpenStack

All of Breqwatr's private clouds run [OpenStack](https://www.openstack.org/software/).

- [Prepare OpenStack Cloud Servers](/openstack-server-setup.html)
- [OpenStack Installation](/openstack-install.html)
    - [Storage - LVM Setup](/openstack-lvm.html)
    - [Storage - Ceph Setup](/openstack-ceph.html)
- [BWDT's OpenStack Command-Line](/openstack-cli.html)
    - [OpenStack CLI Examples](/openstack-cli-examples.html)


