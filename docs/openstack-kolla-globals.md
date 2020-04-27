[Index](/)
\> [OpenStack Installation](/openstack-install.html)
\> Writing globals.yml for Kolla-Ansible

# Writing globals.yml for Kolla-Ansible

The `globals.yml` file is used to specify which OpenStack services will be
installed and how they will be configured.

This file is consumed by [Kolla-Ansible](https://github.com/openstack/kolla-ansible),
a versatile and highly configurable tool for deploying OpenStack services.
With its large range of capabilities comes a fair bit of complexity.

Writing the globals.yml file is arguably the hardest step when deploying
OpenStack. Breqwatr will be releasing tools and documentation to help write
this file in the future, but currently the best approach is to read the
[GitHub template](https://github.com/openstack/kolla-ansible/blob/stable/stein/etc/kolla/globals.yml)
showing the available options. Change the branch to match your release, as some
of the options have changed over time.

Write your `globals.yml` file to define the cloud as you want it, then place it
alongside your passwords.yml file. Be sure to keep a copy of this file
somewhere safe.

For reference, check out these example globals files:

- [Single-node Stein LVM-Backed POC cluster](https://gist.github.com/breqwatr/056bc1d53370a2775d547cac10effa61)
- [Single-node Stein Ceph-backed POC cluster](https://gist.github.com/breqwatr/31fba9b5995e3b9dd1c3673b370aee08)
