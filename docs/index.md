# Breqwatr Deployment Tool

A command-line orchestration toolkit for deploying Breqwatr OpenStack and
its accompanying services.

Breqwatr OpenStack is unmodified OpenStack, but with fully tested and supported
images. Breqwatr also provides custom value-add services to licensed customers.

The Breqwatr Deployment Tool is accessed from the
command line of an Ubuntu based OS using the command `bwdt`.


## Requirements

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
