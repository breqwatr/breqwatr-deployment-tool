[Index](/)
\> [OpenStack Installation](/openstack-install.html)
\> Initialize OpenStack Containers with Kolla-Ansible Deploy

# Initialize OpenStack Containers with Kolla-Ansible Deploy

Everything is ready:

- The [globals file](/openstack-kolla-globals.html) has been written
- The [passwords](/openstack-kolla-passwords.html) are generated
- The [inventory](/openstack-kolla-inventory.html) is written
- The [certificates directory](/openstack-kolla-certificates.html) exists and
  contains the correct certificates - self-signed or otherwise
- Optionally, the [config directory](/openstack-kolla-config.html) contains any
  service files or overrides

Use the following command to deploy OpenStack:

```bash
# Note: --config-dir is optional and can be ommitted

bwdt openstack kolla-ansible deploy \
  --release stein \
  --ssh-private-key-file ~/.ssh/id_rsa \
  --globals-file globals.yml \
  --passwords-file passwords.yml \
  --inventory-file inventory \
  --certificates-dir certificates/ \
  --config-dir config/
```
