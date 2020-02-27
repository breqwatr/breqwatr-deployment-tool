# Installing BWDT

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

## Install from PyPi

To install the current stable version of BWDT, install it uses `pip`. This is
the recommended installation method.

```bash
pip install breqwatr-deployment-tool
```


## Install from GitHub

To install the latest and greatest version of BWDT, you can install directory
from GitHub. This approach is only recommended when Breqwatr support wants you
to use a new feature that isn't formally released.

```bash
pip install git+https://github.com/breqwatr/breqwatr-deployment-tool.git
```


## Install from Offline Media

If you intend to run BWDT in an air-gapped network, you'll want to create
the offline media from an internet-connected network first.

Once you have created your offline install media, it can be used to install
BWDT on the air-gapped systems.

The offline media contains a file named `bwdt.tar.gz`. Unpack it to a
directory off the removable media, then install with this command:

```bash
pip install --no-index --find-links <directory>  breqwatr-deployment-tool
```
