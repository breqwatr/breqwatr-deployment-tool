[Index](/)
\> [OpenStack Installation](/openstack-install.html)
\> OpenStack Post-Deploy Test

# OpenStack Post-Deploy Test

After deploying the cloud, it's important to verify that everything is working.
We've written a test script to spin up a network, image, flavor, volume, and
instance. Once it finishes, you should be able to ping the VM. If the ping
succeeds, the cluster is ready to use.

Make sure tha you've [installed BWDT](/installing-bwdt.html) on the workstation
running these commands, and [downloaded the openrc file](/openstack-kolla-admin-openrc.html).

## Download cirros

```bash
wget -O cirros.qcow2 http://download.cirros-cloud.net/0.5.1/cirros-0.5.1-x86_64-disk.img
```

The image doesn't need to be cirros, but it does need to be a qcow2 format
file.

## Set environment variables

Either a flat or VLAN network are required. If a VLAN network is going to be
used, also set the `VLAN_ID` variable.

**Reminder**: Use FLAT if the switchports attached to the
`neutron_external_interface` are access ports. If they're trunk ports, use
VLAN.

```bash
# Flat example
export NET_TYPE=FLAT

# VLAN example
export NET_TYPE=VLAN
export VLAN_ID=<VlAN ID>
```

Define the CIDR to be used in this network. It will create its own DHCP agent.

```bash
export NET_CIDR=<cidr of the network>
```

Define the default gateway

```bash
export NET_GATEWAY=<ip of default gateway>
```

Set the image path

```bash
export IMG_PATH=<full path to file>
```

Set the path of the openrc file you'll use:

```bash
export OS_OPENRC_PATH=<full openrc file path<
```

Set the OpenStack release that the OpenStack client should run with:

```bash
export OSRELEASE=<openstack release>
```

### Usage sample

```bash
export NET_TYPE=FLAT
NET_CIDR="10.100.104.0/24"
NET_GATEWAY="10.100.104.1"
export IMG_PATH=/home/ubuntu/train/cirros.qcow2
export OS_OPENRC_PATH=/home/ubuntu/train/admin-openrc.sh
export OS_RELEAE=train
```

## Download & run the script

```bash
wget \
  -O test-new-cluster.sh \
  https://gist.githubusercontent.com/breqwatr/364e8aea55db999b527b0d5dee473f6e/raw/a9117974d7030afb06ca21bccb88d4a805d667f3/test-new-cluster.sh

bash test-new-cluster.sh
```


## Ping the VM

From a computer with network access to the FLAT/VLAN network you chose.


## Review the script

If you're curious what the script does, [here it is](https://gist.github.com/breqwatr/364e8aea55db999b527b0d5dee473f6e):

{% gist 364e8aea55db999b527b0d5dee473f6e %}



