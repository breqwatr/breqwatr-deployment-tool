[Index](/)
[\> BWDT's OpenStack Command Line](/openstack-cli.html)
\> OpenStack CLI Examples

# OpenStack CLI Examples

With the exception of image creation, the following `openstack` commands are
shown "raw" and not wrapped in the `bwdt openstack cli` syntax.
For more information about Breqwatr's OpenStack CLI tool, see
[BWDT's OpenStack Command-Line](/openstack-cli.html).

This set of examples isn't nearly exhaustive. Instead, it's meant to illustrate
the basic usage of the OpenStack CLI.

---

# Identity Concepts

## Create a project

Everything in OpenStack belongs to one project or another. Roles are assigned
to users (`admin` and `_member_`) for any project to define what level of
access they have. Note that `admin` access in any project grants cloud-wide
administrative access when a user is scoped to that project.

```bash
openstack project create myproject

# More info:
# openstack project create --help
```


## Create a user

```bash
openstack user create myuser --password 12345

# For more security, prompt for the password
openstack user create myuser --password-prompt

# More info:
# openstack user create --help
```

## Grant a role to a user

Users without any roles on any project can't do anything.

```bash
# show the roles
openstack user role list

# show the users
openstack user list

# show the projects
openstack project list

# Add the member role
openstack role add --user myuser --project myproject _member_
```

### About the admin role

By convention, Breqwatr only grants the admin role to users against the
`admin` project. This makes management easier. Breqwatr's Arcus web UI expects
this convention to be followed.


```bash
# Granting a user cloud-wide administrative access
openstack role add --user myuser --project admin _member_
openstack role add --user myuser --project admin admin
```

When configured this way, users can switch to administrative mode by
setting their `OS_PROJECT_NAME` environment variable/open-rc file line to
`admin`. Note that if you change an open-rc file, you need to `source` it
again.


---


# Images

OpenStack uses images as templates for virtual machine block devices.

Some official OpenStack images can be downloaded [here](https://docs.openstack.org/image-guide/obtain-images.html).


## List current images

Images can be public and available to all projects, or private and only visible
in certain projects. The project your client is scoped to will define the
images output by this command.

```bash
openstack image list
```


## Upload an image

The basic syntax:

```bash
# disk format is usually qcow2 or raw

openstack image create \
  --container-format bare \
  --disk-format <disk format> \
  --file <mounted full path> \
  --public \
  '<image name>'
```

### Downloading a test Cirros image

Cirros is a super-small Linux image that's little more than a network stack.
It's great for testing out OpenStack itself.

```bash
wget wget http://download.cirros-cloud.net/0.5.1/cirros-0.5.1-x86_64-disk.img
```

### Uploading an image to Glance with BWDT

The `bwdt` command supports volume mounts using the `-v` option. It's a direct
pass-through to Docker's `-v` option and uses the same syntax. Launching the
`bwdt openstack cli` with the image mounted inside allows uploading of images
without installing the various OpenStack CLI versions on your workstation.

```bash
# Usage
img_path=$(readlink -f <image file>)

bwdt openstack cli \
  -r <release> \
  -o <openrc file> \
  -v "$img_path:/<mounted full path>" \
  -c "openstack image create --container-format bare --disk-format qcow2 --file <mounted full path> --public '<image name>'"
```

Here's an example:

```bash
# The volume mount needs the full path of the file
img_path=$(readlink -f cirros-0.5.1-x86_64-disk.img)

# Mount the cirros image into the cli container using -v
bwdt openstack cli \
  -r stein \
  -o admin-openrc.sh \
  -v "$img_path:/cirros.img" \
  -c "openstack image create --container-format bare --disk-format qcow2 --file /cirros.img --public 'Cirros'"
```


---

# Networking

## List networking data

Some of these commands may require the admin role.

```bash
openstack network list
openstack subnet list
openstack router list
openstack port list
openstack floating ip list
```


## Creating an external VLAN network

External VLAN networks require that the switches upstream of the OpenStack
nodes are configured to trunk the assigned VLAN ID.

A few notes about VLAN networks:
- By convention, the physical network is always called `physnet1`
- port-security prevents IP masquerading, but it will break virtual appliances
  such as virtual firewalls and load balancers that claim their own IP
  addresses. Users often complain about this feature.

```bash
openstack network create \
  --provider-segment <VLAN ID> \
  --provider-network-type VLAN \
  --provider-physical-network physnet1 \
  --external \
  --disable-port-security \
  <vlan network name>
```


## Creating an external flat network

External flat networks will place VM traffic directly on the host's physical
Neutron-dedicated interface without any encapsulation. In this scenario, the
upstream switchports would be configured as access ports instead of trunks.

```bash
openstack network create \
  --provider-network-type flat
  --provider-physical-network physnet1 \
  --external \
  --disable-port-security \
  <flat network name>

# example
openstack network create \
	--provider-network-type flat \
  --provider-physical-network physnet1 \
  --external \
  --disable-port-security \
  infra-net
```


## Creating an internal VXLAN overlay network

These networks don't exist outside the OpenStack cluster. They span across
all hosts in the cluster and can be defined on-demand without any changes to
the upstream networks. VMs using these networks generally are accessed using
floating IP addresses from an external network.

```bash
openstack network create \
  --provider-network-type vxlan \
  <vxlan network name>

```


## Assign a subnet to a network

Subnets are IP address ranges that can be used inside a network. They can also
support DHCP clients that will be automatically provisioned inside the given
network. Internal VXLAN and external flat / VLAN networks all use the same
subnet syntax.


```bash
openstack subnet create \
  --network <network> \
  --subnet-range <cidr> \
  --allocation-pool start=<ip-address>,end=<ip-address> \
  --gateway <gateway IP \>
  --dhcp \
  <subnet name>

# example
openstack subnet create \
  --network infra-net \
  --subnet-range 192.168.2.0/24 \
  --allocation-pool start=192.168.2.10,end=192.168.2.199 \
  --dhcp \
  infra-subnet
```


## Creating a virtual router

Internal VXLAN overlay networks can't access the LAN outside the OpenStack
cloud on their own, and therefore don't allow their owners to access them. Also
the VMs created on these networks don't have internet access or access to any
other LAN resources. To resolve this limitation, a virtual router should be
created on the VXLAN network to act as the gateway, and that router should be
connected to an upstream external network.

Routers are the logical devices where floating IP addresses will be deployed.

When more than one OpenStack server exists with the network services running on
it, the `--ha` flag can also be used to create a highly available router that
will automatically set up VRRP to ensure availability.

```bash
# create the router
openstack router create <--ha> <name>

# attach the router to a subnet
openstack router add subnet <router name/ID> <subnet name/ID>

# set the upstream network for the router
openstack router set <router> --external-gateway <network>
```

## Creating a floating IP address

Once a server is deployed on an internal VXLAN network, and that network has a
router connected to an external network, a floating IP address can be assigned
to provide inbound access from outside the cloud.

```bash
# create the floating IP
openstack floating ip create <external network name>

# list the floating IP addresses and server ID
openstack floating ip list
openstack server list

# Assign the floating IP to the server
openstack server add floating ip <server name/id> <floating IP address>
```


---

# Flavors

Flavors define the sizes available when creating an instance.

## List current flavors

```bash
openstack flavor list
```


## Create a flavor

```bash
openstack flavor create --disk <size-gb> --vcpus <vcpus> --ram <size-mb> <flavor-name>

# example
openstack flavor create --disk 1 --vcpus 1 --ram 256 tiny
```


---

# Volumes

## Volume types

When an OpenStack cloud is deployed, the Cinder service may be configured with
backing volume types. These are commonly LVM, Ceph, Pure Storage, EMC, or some
other storage appliance.

To list the current volume types:

```bash
openstack volume type list
```

To define a volume type you must be an administrator and should also have SSH
access on the cloud hosts. Modifying the volume types is not done frequently.

```
# the backend-name is defined in cinder-volume's cinder.conf file
openstack volume type create --public --property volume_backend_name='<backend-name>' <name>

# example
openstack volume type create \
  --public \
  --property volume_backend_name='lvm-1' lvm
```


## List volumes

```bash
# show volumes in current project scope
openstack volume list

# scoped as admin, show all volumes
openstack volume list --all
```


## Creating volumes

```bash
# create an empty volume
openstack volume create --type <volume-type>  --size <size in gb> <name>

# Create a boot volume from an image
openstack volume create --type <type> --bootable --image <image> --size <size> <name>

# example
openstack volume create --type lvm --image Cirros --bootable --size 2 cirros-1-boot
```


---


# Servers

## Create a server

There are many ways to create a server. We suggest you first create a bootable
volume from an image, then boot from it.

```bash
# list flavors, networks, images
openstack flavor list
openstack network list
openstack image list

# Creat the server
openstack server create \
  --flavor <flavor> \
  --network <network> \
  --volume <volume> \
  <server name>


# example
openstack volume create --type lvm --image Cirros --bootable --size 2 cirros-1-boot
openstack server create \
  --flavor tiny \
  --network infra-net \
  --volume cirros-1-boot \
  cirros-1


# See also:
# openstack server create --help
```

## Console into a server

Get the console URL, then open it in your browser:

```bash
openstack console url show --novnc <server>
```
