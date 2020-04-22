[Index](/)
[\> Deployment Server](deployment-server.html)
\> Local Apt Service

# Local Apt Service

Breqwatr's local Apt mirror is required for offline installations.

Running the local Apt service also ensures that only tested and confirmed
functional packages are installed on your cloud servers. This helps to avoid
issues where deployment automation that used to work now fails due to a recent
change in dependency packages.

Breqwatr recommends that the local Apt mirror be used for all private clouds
when possible.


## Requirements

The Apt mirror is a Docker image, so it can technically run anywhere Docker is
installed. Since Apt is deployed using BWDT, Ubuntu 18.04 is suggested.

When Breqwatr deploys clouds, we designate one server as the
"[Deployment Server](/deployment-server.md)" and install Apt there.


## Deploying Apt

Run the following command to deploy the apt service on your deployment server:

```bash
# Show the available options
bwdt service apt start --help

# (suggested) - Deploying Apt on port 81 (to not conflict with PXE)
bwdt service apt start --port 81

# Deploying Apt on the standard HTTP port (No PXE on the deployment server)
bwdt service apt start --port 80

# Deploying Apt to host specific packages from an older version
bwdt service apt start --version stable-bionic --port 80
```


## Configure hosts to use local apt

On each cloud host, edit `/etc/apt/sources.list` to use the new private Apt
service.

The following example assumes the deployment server has an IP address of
`10.10.10.9` and the Apt service is running on port 81.

```text
# /etc/apt/sources.list

deb [trusted=yes arch=amd64] http://10.10.10.9:81 bionic main
deb [trusted=yes arch=amd64] http://10.10.10.9:81 bionic-updates main
deb [trusted=yes arch=amd64] http://10.10.10.9:81 bionic-security main
```

Then update your apt cache:

```bash
apt-get update
```

Once that's done, you're ready to use `apt-get install`.

You might see the following warnings. They can safely be ignored:

```text
W: GPG error: http://10.10.111.222:81 bionic InRelease: The following signatures were invalid: 9D2FD3B55183AC63AF0BF44C4BCF2D885010D54A
W: Skipping acquire of configured file 'stable/binary-amd64/Packages' as repository 'http://10.10.111.222:81 bionic InRelease' doesn't have the component 'stable' (component misspelt in sources.list?)
W: Skipping acquire of configured file 'stable/i18n/Translation-en' as repository 'http://10.10.111.222:81 bionic InRelease' doesn't have the component 'stable' (component misspelt in sources.list?)
W: Skipping acquire of configured file 'stable/i18n/Translation-en_US' as repository 'http://10.10.111.222:81 bionic InRelease' doesn't have the component 'stable' (component misspelt in sources.list?)
W: Skipping acquire of configured file 'stable/cnf/Commands-amd64' as repository 'http://10.10.111.222:81 bionic InRelease' doesn't have the component 'stable' (component misspelt in sources.list?)
```
