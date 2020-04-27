[Index](/)
\> [OpenStack Installation](/openstack-install.html)
\> OpenStack Service Configuration

# OpenStack Service Configuration

There are two ways to configure OpenStack's services.

The first and most common method is to modify Kolla-Ansible's [globals file](/openstack-kolla-globals.html).
While the options directly supported by Kolla-Ansible and its
globals file are extensive, they aren't exhaustive. Some configurations, such
as Ceph's keyring files, can't be done this way.

The second approach involves writing your own configuration files. They'll be
merged with those generated by Kolla-Ansible and overwrite any values it had
previously generated. The files are expected to have particular names and exist
in specific directories to function correctly. When deploying a basic LVM
cluster, no custom files need to be written.

To fine-tune the OpenStack services, create a `config/` directory.

This directory will be used with the `bwdt openstack kolla-ansible` command,
specified by the `--config-dir` option.

No specific general customizations are currently recommended, but Ceph-backed
clusters should have already created the files here specified in the
[OpenStack Ceph setup guide](/openstack-ceph.html).
