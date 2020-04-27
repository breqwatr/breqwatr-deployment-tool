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



## Install Guides

- [**Installing Ceph**](/ceph-install.html):
  An open-source cloud storage solution
- [**Installing OpenStack**](/openstack-install.html):
  Private clouds providing virtualisation, SDN, and more


---


# Documentation Index

## BWDT Command-Line Utility

The Breqwatr Deployment Tool is used to deploy and manage all of the software
we support. It's freely available and simple to install.

- [BWDT Installation & Requirements](/installing-bwdt.html)
- [BWDT Services](/bwdt-services.html)
    - [Local Apt Service](/apt.html)
    - [Local Pip Service](/pip.html)
    - [Local Docker Registry](/registry.html)

## Deployment Server

- [Deployment Server](/deployment-server.html)
- [Creating Offline Installation Media](/offline-media.html)

## Ceph

- [Installing Ceph](ceph-install.html)
  - [Prepare Ceph Storage Servers](/ceph-server-setup.html)
  - [Create Ceph-Ansible Configuration Files](/ceph-ansible-configs.html)
  - [Deploy Ceph](ceph-deploy.html)
- Preparing Ceph for OpenStack
    - [Create Ceph's OSD Pools for OpenStack](/ceph-pools.html)
    - [Create CephX Authentication Keys](/ceph-cephx-keys.html)

## OpenStack

- [OpenStack Installation](/openstack-install.html)
    - [Prepare OpenStack Cloud Servers](/openstack-server-setup.html)
    - [OpenStack Storage Providers](/openstack-storage-providers.html)
        - [OpenStack LVM Storage Setup](/openstack-lvm.html)
        - [OpenStack Ceph Setup](/openstack-ceph.html)
    - [Mirroring OpenStack release's images on local registry from Docker Hub](/openstack-registry-mirror.html)
    - [Generate Unique OpenStack Service Passwords](/openstack-kolla-passwords.html)
    - [Writing globals.yml for Kolla-Ansible](/openstack-kolla-globals.html)
    - [Creating Kolla-Ansible's Inventory File](/openstack-kolla-inventory.html)
    - [Configure HTTPS for OpenStack APIs](/openstack-kolla-certificates.html)
    - [OpenStack Service Configuration](/openstack-kolla-config.html)
    - [Kolla-Ansible's Bootstrap Playbook](/openstack-kolla-bootstrap.html)
    - [Pulling Kolla Docker Images to All Servers](/openstack-kolla-pull.html)
    - [Initialize OpenStack Containers with Kolla-Ansible Deploy](openstack-kolla-deploy.html)
    - [Generate admin-openrc.sh](/openstack-kolla-admin-openrc.html)
- [BWDT's OpenStack Command-Line](/openstack-cli.html)
    - [OpenStack CLI Examples](/openstack-cli-examples.html)


