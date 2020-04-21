# Creating CephX Keys for OpenStack

In order for OpenStack's Cinder, Nova, and Glance services to interact with
a secure Ceph cluster, they need to have keys created that grant access to
their respective pools.

If the pools aren't created yet, do that first:
[Creating Ceph's OSD Pools for OpenStack](/ceph-pools.html)


## Show current keys

The `ceph` commandline client is installed and configured with the admin
keyring on any monitor server.


```bash
ceph auth ls
```

## Create new keys

Create keys for Cinder, Glance, and Nova. Grant them the capabilities required
for OpenStack against the volumes and images pools.

```bash
ceph auth get-or-create client.glance
ceph auth caps client.glance \
  mon 'allow r' \
  mds 'allow r' \
  osd 'allow rwx pool=volumes, allow rwx pool=images, allow class-read object_prefix rbd_children'

ceph auth get-or-create client.cinder
ceph auth caps client.cinder\
  mon 'allow r' \
  mds 'allow r' \
  osd 'allow rwx pool=volumes, allow rwx pool=images, allow class-read object_prefix rbd_children'

ceph auth get-or-create client.nova
ceph auth caps client.nova \
  mon 'allow r' \
  mds 'allow r' \
  osd 'allow rwx pool=volumes, allow rwx pool=images, allow class-read object_prefix rbd_children'
```

## Show existing keyrings

To show the keyrings that were created, for instance to pipe them to a file,
use `ceph auth get`.

```bash
ceph auth get client.glance
ceph auth get client.cinder
ceph auth get client.nova
```
