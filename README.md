# Breqwatr Deployment Tool


## Install

### From PyPi

```python
pip install breqwatr-deployment-tool
```

### From GitHub

```python
pip install git+https://github.com/breqwatr/breqwatr-deployment-tool.git
```


## Examples

### Help

```bash
bwdt --help
```

### Registry

Start the registry service

```bash
bwdt registry start
```

Sync an OpenStack image from Breqwatr's upstream online registry to a  locally
hosted registry.

```bash
bwdt registry sync-openstack-image <registry url> <image name>
```

Sync all the required images for an OpenStack deployment to a local registry.

```bash
bwdt registry sync-all-openstack-images <registry url>
```

List the images in a local registry and their tags

```bash
bwdt registry list-images <registry url>
```

### Launch PXE

Example of launching the PXE service:

```bash
bwdt pxe start --interface enp0s25 --dhcp-start 10.1.0.90 --dhcp-end 10.1.0.99
```

### Arcus

Arcus is the custom web UI Breqwatr uses to replace Horizon.

Initialize the datbase for the Arcus service:

```bash
bwdt arcus database-init --host <host> --admin-user root --admin-pass <password> --arcus-pass <password>
```

Create the Openstack service account for Arcus:

```bash
bwdt arcus create-service-account --cloud-fqdn <fqdn or vip> --bootstrap-password <password of bootstrap user> --sa-password <password for arcus SA>
```

