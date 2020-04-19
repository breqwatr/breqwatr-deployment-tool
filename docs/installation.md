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

### Installing Docker

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
apt-get update
apt-get install -y docker-ce
```

### Python Pip

Pip is the primary package management utility for Python.

Since BWDT requires Python 3, pip for Python 3 is required to install the
Breqwatr Deployment tool. Be careful not to use pip for Python 2.

```bash
apt-get install python3-pip
```

### Virtualenv

We suggest you use a `virtualenv` to install BWDT. If you're not familiar with
the procedure, it can be set up as follows.

Be sure to source into your virtualenv before attempting to run the `bwdt`
command line. This will need to be re-done in each new terminal session.

```bash
# Install virtualenv for python 3 if it isn't installed yet
apt-get install python3-virtualenv virtualenv

# Create the virtual environment
virtualenv --python=python3 env/

# Use ("activate") the virtual environment
source env/bin/activate

# When you're done, "deactivate" to exit the virtualenv
deactivate
```

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
