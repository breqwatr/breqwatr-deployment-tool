# Breqwatr Deployment Tool

A command-line driven deployment toolkit for containerized, open source cloud
services such as OpenStack and Ceph. BWDT can also deploy various other
services to enable air-gap/dark-site installations such as private Apt and Pip
repositories.

The Breqwatr Deployment Tool (BWDT) enables an offline, reliable, and easy
installation procedure for what are otherwise highly complicated tools.

Breqwatr builds, hosts, and supports Docker images that are known to work well
with each-other and are easy to support. The BWDT command line is built to
deploy, launch, and manage those containerised services.

With the exception of a few value-add services, namely Arcus and Support, all
Breqwatr tools are free and open source. You can use BWDT to deploy OpenStack
and Ceph in your environment without purchasing a license, though the images
will come from Docker Hub instead of Breqwatr's registry and might be a bit
older.



## Requirements

The Breqwatr Deployment Tool is accessed as a python-driven command line. It
runs on an Ubuntu server based OS, and is launched using the command `bwdt`.

To use the Breqwatr Deployment Tool CLI, the following requirements must be
present on the system where BWDT will run.

- Ubuntu 18.04 or later
- Docker
- Python 3
- Offline install requires a removable drive (such as a USB thumb-drive)
- Licensed features require a Breqwatr Cloud License Key


---


# Installing BWDT

## From PyPi

```bash
pip install breqwatr-deployment-tool
```

## From GitHub

```bash
pip install git+https://github.com/breqwatr/breqwatr-deployment-tool.git
```

## From Offline Media

If you intend to run BWDT in an air-gapped network, you will want to create
your offline media from an internet-connected network first. Once you have
created your offline install media, it can be used to install BWDT on the
air-gapped systems.

The offline media contains a file named `bwdt.tar.gz`. Unpack it to a
directory off the removable media, then install with this command:

```bash
pip install --no-index --find-links <directory>  breqwatr-deployment-tool
```
