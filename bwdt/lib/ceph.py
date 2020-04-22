""" Ceph deployment and management """
import sys

import bwdt.constants as constants
import bwdt.lib.docker as docker
from bwdt.lib.common import volume_opt


def ceph_ansible_exec(release, inventory_path, group_vars_path, ssh_key_path):
    """ Execute ceph-ansible commands """
    if release not in constants.CEPH_RELEASES:
        err = (f'ERROR: Invalid release "{release}" - '
               f'Valid releases: {constants.CEPH_RELEASES}\n')
        sys.stderr.write(err)
        sys.exit(1)
    docker.get_image('ceph-ansible', release)
    run_cmd = ('ansible-playbook '
               '-i /ceph-inventory.yml '
               '/var/repos/ceph-ansible/site.yml')
    cmd = (f'docker run --rm --network host --workdir /var/repos/ceph-ansible '
           + volume_opt(inventory_path, '/ceph-inventory.yml')
           + volume_opt(ssh_key_path, '/root/.ssh/id_rsa')
           + volume_opt(group_vars_path, '/var/repos/ceph-ansible/group_vars')
           + f'{constants.IMAGE_PREFIX}/ceph-ansible:{release} {run_cmd}')
    docker.shell(cmd)



