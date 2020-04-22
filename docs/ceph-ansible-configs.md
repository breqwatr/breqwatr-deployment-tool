[Index](/)
\> Ceph-Ansible Configuration Files

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


{% gist de9ed062c773768c418da91e23733492 %}


## The group\_vars Directory

The `group_vars` directory is an Ansible convention used to define and override
values used by Ansible's playbooks. Ceph-Ansible supports several files which
can alter how the playbooks operate.

This [GitHub page](https://github.com/ceph/ceph-ansible/tree/stable-5.0/group_vars)
is a good reference for the sample files.
The [official documentation](https://docs.ceph.com/ceph-ansible/master/) also
covers these files in some detail.

General speaking we only set a few values in two of these files and leave the
rest as their defaults.

Create the following files:

- `group_vars/all.yml`
- `group_vars/osds.yml`


### all.yml

{% gist 3f30e1659a45fb3976654e1771fe5327 %}


### osds.yml

{% gist 6786866104c91fe95b9e802b23d43ccc %}
