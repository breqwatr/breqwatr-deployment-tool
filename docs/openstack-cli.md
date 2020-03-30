# BWDT's OpenStack Command Line

Breqwatr distributes a pre-packaged command-line container that can be easily
used with `bwdt`. The main advantage of this approach over local installation
(`pip install python-openstackclient`) is that you don't need to install any
dependencies and the client will always be built for the appropriate OpenStack
release.


## OpenRC File

The OpenStack client has three ways to be configured.

1. interactive arguments on each call: `--os-username`, and so on
1. A YAML file stored in a specific directory
1. An OpenRC file exporting environment variables

**Breqwatr is standardized on the OpenRC file.**

In a Breqwatr-deployed cloud you can generate an initial OpenRC file for the
bootstrap admin user from `bwdt`:

```bash
bwdt openstack get-admin-openrc
```

In general you'll want to scope to your own user though. To do so, write
an openrc file.

```
# Enter your data <here>
export OS_PROJECT_NAME=<project to scope to>
export OS_USERNAME=<your username>
export OS_PASSWORD=<your password>
export OS_AUTH_URL=https://<OpenStack URL>:5000/v3

# These don't normally need to change
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3
export OS_REGION_NAME=RegionOne
```

## Using the OpenStack client

```bash
# Launch the interactive client
bwdt openstack cli --release stein --openrc-path admin-openrc.sh

# Shorthand argument example
bwdt openstack cli -r stein -o admin-openrc.sh

# Execute a command inside the container
bwdt openstack cli -r stein -o admin-openrc.sh -c "openstack network list"
```

The `cli` command also supports its own environment variables, so the release
and openrc file don't need to be specified each call.

```bash
# set environment variables
export OS_RELEASE=stein
export OS_OPENRC_PATH=/home/myuser/admin-openrc.sh

# interactive CLI
bwdt openstack cli

# execute one command - don't forget the quotes
bwdt openstack cli -c "openstack flavor list"
```

**Mounting files into the CLI container**
```bash
# Don't forget the quotes
bwdt openstack cli -v "<full path of file/directory>:<mount path>"

**Treating the Openstack CLI like a VM**

It can be convenient to just hop right into the CLI container for certain
use-cases.

```bash
bwdt openstack cli -c bash
# For the openstack command to work, source its environment
source /var/repos/env/bin/activate
```


---


For more information regarding how to operate OpenStack from the command-line,
check out our [OpenStack CLI Examples](/openstack-cli-examples.html).
