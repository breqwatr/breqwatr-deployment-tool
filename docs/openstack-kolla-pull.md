[Index](/)
\> [OpenStack Installation](/openstack-install.html)
\> Pulling Kolla Docker Images to All Servers

# Pulling Kolla Docker Images to All Servers

The various processes/services that makes up OpenStack are packaged into
their own Docker image. These images will be deployed and configured by the
Kolla-Ansible project's automation.

At this point in the deployment, the [local registry](/registry.html) is
running and the Kolla images are [synchronized to it](/openstack-registry-mirror.html).

The next step is to download each image to the OpenStack servers which will
run them. Kolla-Ansible's "deploy" task would also do pull the images, but
doing so ahead of time helps identify any missing images without getting stuck
with a half-deployed cloud.

``bash
bwdt openstack kolla-ansible pull \
  --release stein \
  --ssh-private-key-file ~/.ssh/id_rsa \
  --globals-file globals.yml \
  --passwords-file passwords.yml \
  --inventory-file inventory \
  --certificates-dir certificates
```

