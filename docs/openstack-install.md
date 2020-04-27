[Index](/)
\> OpenStack Installation

# OpenStack Installation

All of Breqwatr's private clouds run [OpenStack](https://www.openstack.org/software/).

There's no one "right" way to install OpenStack. Breqwatr's procedure has
been repeatedly tested, used in production, and enterprise support is
available.

Breqwatr has selected a subset of the OpenStack ecosystem to support
and distribute to ensure that while not every possible service is available,
the supported ones are production-ready at all times.

Currently Breqwatr has standardized on the
[Kolla-Ansible](https://github.com/openstack/kolla-ansible) project and its
[Kolla](https://github.com/openstack/kolla)-based images to deploy and manage
OpenStack. The Breqwatr Deployment Tool has integrated these libraries to
improve ease-of-use. Breqwatr distributes known-stable builds Kolla images,
with only minor customization such as the introduction of various Cinder-volume
plugins.


Deployment scenarios vary widely. These guides hope to cover the most common
scenarios. For more complicated scenarios Breqwatr offers training,
professional services, support, and managed services - [contact us](mailto:sales@breqwatr.com)
to learn more.


---


# Installation Procedure

## Online Install with Ceph Storage

This installation procedure is our most common use-case. It requires that
Ceph already be installed. If you haven't installed Ceph yet, follow the
[Ceph install guide](/ceph-install.html) first.

1. [**Create a Deployment Server**](/deployment-server.html): A stand-alone Ubuntu
   server with network access to each OpenStack node should be dedicated to
   deploying and managing the cluster. This is typically the same server that
   was used to deploy Ceph.
1. [**Prepare the metal cloud servers**](/openstack-server-setup.html):
   Metal servers need their OS deployed and some initial setup
1. [**Launch a local Docker Registry**](/registry.html): Without a local cache of
   the docker images, each server will have to download the images from the
   internet. The Train release can have upwards of 90 images when everything is
   enabled, so it's much better to download the images once to a local
   registry.
1. [**Copy images from Docker Hub to the local registry**]((/openstack-registry-mirror.html):
   BWDT will orchestrate the synchronization of a given OpenStack releases
   images to the locally deployed registry.
1. [**Create Ceph OSD pools for OpenStack**](/ceph-pools.html): Two Ceph pools,
   usually `volumes` and `images` will be created for OpenStack.
1. [**Create cephx authentication keys**](/ceph-cephx-keys.html): Keys for the
   Cinder, Nova, and Glance services will be created and granted access to the
   above pools.
1. [**Generate unique passwords for OpenStack service**](/openstack-kolla-passwords.html):
   Create a passwords file named `passwords.yml` to provide each OpenStack
   service with unique passwords.
1. [**Create globals.yml for Kolla-Ansible**](/openstack-kolla-globals.html):
   Define which OpenStack services will be deployed and how they will be
   configured using the `globals.yml` file.
1. [**Write the inventory file for Kolla-Ansible**](/openstack-kolla-inventory.html):
   Define which physical servers will host what OpenStack roles using by
   generating an `inventory` file from a template then populating it.
1. [**Configure HTTPS for Kolla-Ansible**](/openstack-kolla-certificates.md):
   If needed, self-signed certificates are generated. Certificate files are
   prepared for Kolla-Ansible to use with each OpenStack API, enabling HTTPS.
1. [**Fine-tune the OpenStack configuration**](/openstack-kolla-config.html):
   Write service configuration override files into a configuration directory
   `config/`. These are configurations that Kolla-Ansible's globals file cannot
   make on its own.
1. [**Bootstrap the metal servers for OpenStack**](/openstack-kolla-bootstrap.html):
   Install Docker and other packages on the servers that will host OpenStack
   using Kolla-Ansible's bootstrap playlist.
1. [**Pull Docker images to each node**](/openstack-kolla-pull.html):
   Download the Docker images to each OpenStack server.
1. [**Initialize OpenStack's service containers**](/openstack-kolla-deploy.html):
   Launch Kolla-Ansible's deploy playbooks to write the OpenStack configuration
   files on each server and initialize the OpenStack service containers.

---

# Post-Installation Procedure

1. [**Generate the admin user's admin-openrc file**](): OpenStack deploys with a
   single user named "admin". Create an openrc file to use the CLI as this
   user.
