[Index](/)
\> Preparing Ceph for OpenStack
\> Creating Ceph’s OSD Pools

# Creating Ceph's OSD Pools

Ceph creates block devices in pools. For OpenStack, at least two pools will be
created:

- volumes
- images

## List current pools

Before creating any pools, list the current pools:

```bash
ceph osd lspools
```

Don't worry about any default pools, they'll use hardly any data.

## Calculate placement groups

Ceph splits its data into objects that are stored in placement groups. Each
pool is created with a set number of placement groups depending on the number
of OSDs which will use that pool and the replica count (size) of the pool.

1. [Open ceph.io's pg calculator](https://ceph.io/pgcalc/)
1. Delete the pools that listed by default using the trash icon to the left
1. Click the Add Pools button to add a pool
    1. Add two pools, `volumes` and `images`
    1. **Size**: your replica count -
       usually either 2 or 3 depending on whether you're using SSD or HDD
    1. **OSD #** is the number of OSD drives in your cluster that this pool will
       use. By default it will use all the drives.
    1. **% Data**: Set volumes to 80 and images to 20
    1. **Target PGs per OSD**: 200


### Sample PG counts

- For a very small 1-node 1-disk POC cluster
    - **images**: 32
    - **volumes**: 128
- For a generic POC cluster of 4 nodes with size=3 and 24 drives total
    - **images**: 256
    - **volumes**: 1024


## Create Pools

SSH into one of the Ceph monitor servers, it will have the client already
installed and configured.

Create the volumes and images pools:

```bash
ceph osd pool create volumes <volumes pg count>
ceph osd pool set volumes size <replica count>
ceph osd pool application enable volumes rbd

ceph osd pool create images <volumes pg count>
ceph osd pool set images size <replica count>
ceph osd pool application enable images rbd
```