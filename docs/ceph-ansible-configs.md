# Ceph-Ansible Configuration Files


Before you can run Ceph-Ansible to deploy your cluster, you need to define
its configuration. You need 3 things:

1. An SSH Private key (`ssh-keygen`)
1. An inventory file for Ansible
1. A `group_vars` directory containing at least `all.yml` and `osds.yml`.


## Inventory

The inventory file defines which servers will own what roles in your cluster.
Each server listed in the inventory must have an entry in their
`/root/.ssh/authorized_keys` file and permit Ceph-Ansible to SSH as root.

For a summary of what each service does, check [Ceph's documentation](https://docs.ceph.com/docs/mimic/start/intro/).

By convention, we name this file `ceph-inventory.yml`.

```yaml
# ceph-inventory.yml

all:
  children:
    # These servers host the monitor service
    mons:
        hosts:
          # List the hostnames and their IP addresses as follows
          # You can define multiple hosts this way.
          controlServerHostname1:
            ansible_host: < server1_ssh_mgmt_ip >
            monitor_address: < server1_monitor_ip >
          controlServerHostname2:
            ansible_host: < server2_ssh_mgmt_ip >
            monitor_address: < server2_monitor_ip >
          controlServerHostname3:
            ansible_host: < server3_ssh_mgmt_ip >
            monitor_address: < server3_monitor_ip>
    mgrs:
        hosts:
          controlServerHostname1:
            ansible_host: < server1_ssh_mgmt_ip >
          controlServerHostname2:
            ansible_host: < server2_ssh_mgmt_ip >
          controlServerHostname3:
            ansible_host: < server3_ssh_mgmt_ip >

    # These servers host the Object Storage Daemon service
    osds:
        hosts:
          osdServerHostname4:
            ansible_host: < server4_ssh_mgmt_ip >
            # OSD drives - cluster data is stored on these
            # sda, sdb, and sdc are just examples. Use fdisk -l to find yours.
            devices:
              - /dev/sda
              - /dev/sdb
              - /dev/sdc
            # (optional) Dedicated ROCKSDB & WAL drives. If used, this must
            # have the same # of entries as {{devices}}. Each index matches
            # up. Devices can and usually are reused.
            dedicated_devices:
              - /dev/sdd
              - /dev/sdd
              - /dev/sdd
          osdServerHostname5:
            ansible_host: < server5_ssh_mgmt_ip >
            # OSD drives - cluster data is stored on these
            devices:
              - /dev/sda
              - /dev/sdb
              - /dev/sdc
            # (optional) Dedicated ROCKSDB & WAL drives. If used, this must
            # have the same # of entries as {{devices}}. Each index matches
            # up. Devices can and usually are reused.
            dedicated_devices:
              - /dev/sdd
              - /dev/sdd
              - /dev/sdd

    # These servers host the Rados Gateway service
    rgw:
        hosts:
          controlServerHostname1:
            ansible_host: < server1_ssh_mgmt_ip >
          controlServerHostname2:
            ansible_host: < server2_ssh_mgmt_ip >
          controlServerHostname3:
            ansible_host: < server3_ssh_mgmt_ip >

    # These service host the MetaData service
    mdss:
        hosts:
          controlServerHostname1:
            ansible_host: < server1_ssh_mgmt_ip >
          controlServerHostname2:
            ansible_host: < server2_ssh_mgmt_ip >
          controlServerHostname3:
            ansible_host: < server3_ssh_mgmt_ip >
```


## The group_vars Directory

The `group_vars` directory is an Ansible convention used to define and override
values used by Ansible's playbooks. Ceph-Ansible supports several files which
can alter how the playbooks operate.

This [GitHub page](https://github.com/ceph/ceph-ansible/tree/stable-5.0/group_vars)
is a good reference for the sample files.
The [official documentation](https://docs.ceph.com/ceph-ansible/master/) also
covers these files in some detail.

General speaking we only set a few values in two of these files and leave the
rest as their defaults.


### all.yml

```yaml
--
# all.yml
# https://github.com/ceph/ceph-ansible/blob/master/group_vars/all.yml.sample

# Choose your release [luminous, mimic, nautilus, octopus]
ceph_stable_release: luminous

# cephx should be enabled - it provides authentication to the cluster
cephx: true

# The ceph monitor service will be configured to bind to any IP address found
# in the given subnet. Use CIDR notation (ex. 192.168.1.0/24)
monitor_address_block: {{ minitor_cidr }}

q# radosgw_address_block works the same as monitor_address_block, but it is used
# for the Rados Gateway service configuration.
radosgw_address_block: {{ ceph_cidr }}

# The Ceph services will listen on this subnet for ceph clients to connect
public_network: {{ ceph_cidr }}

# Optionally, a private network can be specified to segregate internal cluster
# traffic.
cluster_network: {{ ceph_cidr }}

# The objectstore can be filestore or bluestore. Unless deploying a very old
# version of Ceph, use bluestore.
osd_objectstore: bluestore


ceph_conf_overrides:
  global:

    # Set the default PG count nice and low.
    osd_pool_default_pg_num: 32
    osd_pool_default_pgp_num: 32

    # How many data replicas (osd_pool_default_size)?
    #   1: for single-node POC cluster or clusters where data redundancy isn't
    #      required. Note that any disk failure will probably wreck the whole
    #      cluster.
    #   2: For All-SSD pools
    #   3: For pools with HDDs
    osd_pool_default_size: 2

    # Allowing pool deletion is helpful but might not be wanted in production
    mon_allow_pool_delete: true

    # Default is 200, 300 helps in smaller clusters
    mon_max_pg_per_osd: 300


# If using private apt, ceph_ansible needs to redefine the apt source to point
#   to the local mirror. ceph_origin, ceph_repository, and ceph_custom_repo
#   should be set as follows:
# ceph_origin: repository
# ceph_repository: custom
# ceph_custom_repo: "[trusted=yes arch=amd64] http://{{ apt_repo_url }}:{{ apt_repo_port }}"


# If you're deploying a small cluster with a lot of PGs that you intend to grow
#   soon, you might want to disable the max PG per OSD warning.
#   Warning: This is usually a bad idea.
# mon_pg_warn_max_per_osd:0

```


### osds.yml

```yaml
---
# Reference:
# https://github.com/ceph/ceph-ansible/blob/master/group_vars/osds.yml.sample

# By default the admin key isn't distributed to OSD nodes since they don't
# really need it, but it makes administration easier to have it there.
copy_admin_key: true

# If you've defined dedicated_devices in the inventory to use sort of like a
# cache, then set this to "non-collocated". "collocated" puts the ROCKSDB/WAL
# on the same drive as the data.
osd_scenario: "collocated"


# Set devices but leave it empty. The auto-discovery is dangerous so we define
# the disks in the inventory, per-host
devices:
osd_auto_discovery: false
```
