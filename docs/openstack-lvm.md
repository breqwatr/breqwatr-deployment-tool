[Index](/)
\> [OpenStack Installation](/openstack-install.html)
\> [OpenStack Storage Providers](/openstack-storage-providers.html)
\> OpenStack LVM Setup

# OpenStack LVM Storage Setup

OpenStack nodes can use their local disks for cloud storage. An LVM
volume group is presented to OpenStack's Cinder service, and logical volumes
are carved out one per block device.

Using LVM storage has several advantages:

- **Low cost**: Dedicated storage servers or appliances are not needed.
- **Simple to set up & maintain**: LVM is a widely used and understood
  technology with minimal learning curve and abundant documentation.
- **Low latency**:  When guests are on the same server as the LVM disks, they
  have extremely low IO latency. This is particularly useful in VDI scenarios.
- Suitable for small clusters and proofs-of-concept

The most notable disadvantages of LVM are:

- **Non-replicated**: Unless you've used RAID for these disks, their data is
  not preserved when a disk fails.
- **Difficulty with migrations**: OpenStack handles guest migrations between
  hosts differently with shared vs non-shared storage. Shared storage works
  better.
- **Host-based availability**: If the node itself dies, for instance due to a
  hardware failure or corruption of the OS volume, all LVM-based cloud volumes
  on that node become inaccessible. Solutions such as Ceph or storage
  appliances do not have this limitation.


## LVM Configuration

Choose a volume group name. By default, we use `cinder-volumes`.

The actual configuration is fairly straightforward. This does require dedicated
disks, you shouldn't use a volume-group that's already in-use by the OS, for
instance.

Run the following commands on each OpenStack node which will provide storage,
"storage node".

Here's an example of creating a single-disk volume-group:

```bash
# List your drives
fdisk -l

# Identify the drive to be used. Example: /dev/sdb

# Create a phsical volume in LVM
pvcreate /dev/sdb

# Confirm the physical volume was created by listing them
pvdisplay

# Create the volume group
vgcreate cinder-volumes /dev/sdb

# Confirm the volume group was created
vgdisplay
```

Later, after volumes for VMs have been created, you can see them in LVM as
logical volumes.

```bash
lvdisplay cinder-volumes
```
