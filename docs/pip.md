# Local Pip Service

Pip is the package management service for Python. Breqwatr uses several Python
applications to deploy and manage OpenStack and Ceph in particular.

The local Pip service is required When deploying cloud services in an
offline/air-gapped environment.

The Pip service is available For environments where each cloud server has
outbound internet access too, as it can ensure that only confirmed & tested
packages are available. This can prevent the installation prodedure from
failing due to an issue with a new python package release.


## Requirements

The pip service is a Docker image, so it can technically run anywhere Docker is
installed. Since Pip is deployed using BWDT, Ubuntu 18.04 is suggested.

When Breqwatr deploys clouds, we designate one server as the
"[Deployment Server](/deployment-server.md)" and install Pip there.


## Deploying Pip

Run the following command to deploy the pip service on your deployment server:

```bash
# Show the available options
bwdt service pip start --help

# Start the pip service
bwdt service pip start

# (alternatively) Start pip with a specific version
bwdt service pip start --version stable
```


## Configuring servers to use local pip

By default, servers will try to use the public PyPi servers when the `pip`
command is ran. To redirect them to use the local pip server, edit
`/etc/pip.conf` and set it as follows:

```ini
# /etc/pip.conf

[global]
trusted-host = <Deployment server IP>
index-url = http://<Deployment server IP>:3141/root/pypi/+simple/

[search]
index = http://<Deployment server IP>:3141/root/pypi/
```
