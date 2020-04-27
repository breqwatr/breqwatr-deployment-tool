[Index](/)
\> [OpensStack Installation](/openstack-install.html)
\> OpenStack Storage Providers

# OpenStack Storage Providers

OpenStack instances can be created either with ephemeral storage or using the
[Cinder](https://wiki.openstack.org/wiki/Cinder) volume service's block
devices.

Breqwatr recommends to always use Cinder volumes for all instances created on
OpenStack.

To enable cinder volumes, at least one backing storage provider must be
configured. For a full list of supported storage drivers, reference the
[Cinder support matrix](https://docs.openstack.org/cinder/latest/reference/support-matrix.html).

With the Breqwatr Deployment Tool, our most commonly used storage providers
are simple to configure.


## Ceph

OpenStack and Ceph are very frequently deployed together. The Cinder service
even has some optemizations with Ceph to help create VMs faster. Unless a
supported enterprise storage appliance is already deployed, we suggest you
use Ceph to b back your volumes.

Instead of iSCSI, Ceph uses its own RADOS client protocol and interacts with
RBDs (Rados Block Devices). These block devices are carved from the total
available cluster are automatically replicate according to the Ceph pool's
configured rules.

[Ceph Setup](/openstack-ceph.html)


## LVM

Each OpenStack server with the storage role will expose a named LVM volume
group to the cluster. Logical volumes are accessed using iSCSI and mounted to
the created instances.

Generally LVM is chosen for very small clusters that don't need HA. Breqwatr
frequently uses LVM storage for one-off developer clusters and testing. Another
use-case for LVM is when paired with low-latency SSDs for maximum performance,
as it outperforms Ceph at the cost of features and availability.

[LVM Setup](/openstack-lvm.html)


