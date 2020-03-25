# OpenStack Installation

There are many varying ways to configure OpenStack, each depending on the
physical equipment available and desired features to be deployed. Breqwatr
takes an opinionated approach, only offering the services we're comfortable
supporting but also ensuring that each of those features is stable and
reliable.


## Procedure

1. Configure storage providers
1. Load the Ansible image used to deploy OpenStack
1. Generate a passwords file - `passwords.yml`
1. Write your "globals" configuration file - `globals.yml`
1. Write the inventory file - `inventory`
1. Deploy/generate HTTP certificate files - `certificates/`
1. (optional) Write service configuration files - `config/`
1. Bootstrap OpenStack nodes
1. Pull Docker images to each node
1. Deploy OpenStack
1. Get admin-openrc file


---


## Configuring storage providers

OpenStack Cinder supports a long list of storage backends.

[See the Cinder support matrix](https://docs.openstack.org/cinder/rocky/reference/support-matrix.html).

Breqwatr primarily deploys using Ceph, LVM, and Pure Storage as our back-end
plugins of choice. The Cinder-volume container we publish to Docker Hub hosts
all of these. Customer images from our private repository may have other
plugins supported as well.

Choose your storage provider and configure it.
## Loading the Kolla-Ansible image

Breqwatr currently uses Kolla-Ansible for its OpenStack deployments. We've
containerized it for portability and ease of use. This image needs to be
present on the deployment server before OpenStack can be deployed.

```bash
bwdt openstack pull-kolla-ansible --release <release name>
```

- [LVM Setup Guide](openstack-lvm.html)


## Generating passwords.yml

Each OpenStack service and underlying infrastructure component requires
authentication. To prevent password re-use, the passwords need to be generated
separately for each cluster. The passwords will be stored in a file called
`passwords.yml`, which should be kept backed up in a safe location after the
deployment.

To generate `passwords.yml`:

```bash
# This will create ./passwords.yml
bwdt openstack generate-passwords --release <release name>
```


## Writing globals.yml

This is arguably the hardest step when deploying OpenStack. Breqwatr will be
releasing tools to help write this file in the future, but currently the best
approach is to read the [GitHub template](https://github.com/openstack/kolla-ansible/blob/stable/stein/etc/kolla/globals.yml)
showing the available options. Change the branch to match your release, as some
of the options have changed over time.

Write your `globals.yml` file to define the cloud as you want it, then place it
alongside your passwords.yml file. Be sure to keep a copy of this file
somewhere safe.


## Writing the inventory file

The inventory file defines which nodes will run what OpenStack roles.

Generate a template of the file. The following command will create the file
`./inventory`.

```bash
bwdt openstack get-inventory-template --release stein
```

This is a standard Ansible inventory file. It is not necessary to be familiar
with Ansible to work with this file.

The general format is:

```ini
[<role>]
<hostname>      <additional properties>

# example
[control]
localhost       ansible_connection=local
```

Edit the template to list each hostname under each role it will operate.
In small clusters, you can list the same few nodes for each role and it will
work just fine. Larger clusters benefit from increased segregation of
responsibilities.

No additional properties (such as `ansible_connection=local`) are required.

```ini
[control]
controlNode1
controlNode2
controlNode3

[network]
controlNode1
controlNode2
controlNode3

[compute]
computeNode1
computeNode2
computeNode3
computeNode4
computeNode5

[storage]
storageNode1
storageNode2
storageNode3

[monitoring]
controlNode1
controlNode2
controlNode3
```

In the deployment server, now's a good time to double-check that you can
ping each of those hostnames. The deployment will fail if your DNS or
`/etc/hosts` file aren't set up correctly.

Similarly, SSH to each server using your designated SSH key as root to
confirm that the `authorized_keys` files are deployed correctly.


## Deploy/generate HTTPS certificate

While technically optional, OpenStack should always be deployed to use HTTPS
on its API endpoints. Breqwatr does not support non-HTTPS deployment models.

HTTPS is enabled by setting the following in `globals.yml`:

```yml
kolla_enable_tls_external: yes
```

Certificates are deployed in a `certificates` directory.

By default Kolla-Ansible will look for the following two files:

- **certificates/haproxy.pem**: This is the public and private certificate
  combined.
- **certificates/ca/haproxy.crt**: When applicable, this is the certificate
  authority certificate.

The filenames can be modified in `globals.yml`.

### Generate self-signed certificates

Use the `generate-certificates` command to generate new self-signed
certificates. A new directory named `certificates/` will be created in the
directory specified by `--config-dir`.

```bash
# creates ./certificates/
bwdt openstack generate-certificates \
  --release stein \
  --globals-file globals.yml \
  --passwords-file passwords.yml
```

### Using your own certificates

Instead of generating the self-signed certificates, copy your valid ones into
the `config/certificates/` directory with the correct filenames.

```bash
mkdir certificates/
cp <valid certificate file path> haproxy.pem
```


### Writing the optional service configuration files

The default configurations will be sufficient for most use cases but in some
situations a specific OpenStack service configuration change is needed. To
facilitate those changes, a configuration directory can be created.


You can read more about how to write these files and their expected
directory structure in [Kolla-Ansible's advanced configuration guide](https://docs.openstack.org/kolla-ansible/latest/admin/advanced-configuration.html).

This configuration directory will be mounted to Kolla-Ansible's
`/etc/kolla/config` directory when executing the `deploy` and `reconfigure`
tasks.


## Bootstrap OpenStack nodes

The servers that will host OpenStack services should now be online and have
their networks and SSH `authorized_keys` files configured, but they need
Docker and some other packages to be fully ready to launch the OpenStack
containers. The bootstrap step will finalize their preparation.

When setting up the deployment server, an SSH key-pair was created. By default
this will be placed in `~/.ssh/id_rsa` but its location can vary.

```bash
bwdt openstack bootstrap \
  --release stein \
  --ssh-private-key-file ~/.ssh/id_rsa \
  --globals-file globals.yml \
  --passwords-file passwords.yml \
  --inventory-file inventory
```

## Pull OpenStack images to nodes

Each process or service that makes up OpenStack is packaged into its own Docker
image. These images will be deployed and configured by the Kolla-Ansible
project's automation.

To prevent the installation from failing mid-automation due to a missing image,
you should pull the images to each node first. Pass the inventory file path to
the `pull-images` command to let Ansible know which nodes need which service
images.

```bash
bwdt openstack pull-images \
  --release stein \
  --ssh-private-key-file ~/.ssh/id_rsa \
  --globals-file globals.yml \
  --passwords-file passwords.yml \
  --inventory-file inventory
```


## Deploy OpenStack

Everything is ready, now create the OpenStack containers and initialize each
service using the `deploy` command.

```bash
bwdt openstack deploy \
  --release stein \
  --ssh-private-key-file ~/.ssh/id_rsa \
  --globals-file globals.yml \
  --passwords-file passwords.yml \
  --inventory-file inventory \
  --certificates-dir certificates

# Optionally:  --config-dir config
```


## Get admin-openrc file

The admin-openrc file is used to authenticate as the default administrative
service account in OpenStack. This account is used to bootstrap other services
and create the initial regular users.

```bash
bwdt openstack get-admin-openrc \
  --release stein \
  --globals-file globals.yml \
  --passwords-file passwords.yml \
  --inventory-file inventory
```
