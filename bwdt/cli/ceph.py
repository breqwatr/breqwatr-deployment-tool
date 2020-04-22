""" Commands for setting up ceph """

import click

import bwdt.constants as constants
import bwdt.lib.ceph as ceph


def get_ceph_group():
    """ Return the Ceph click group """
    @click.group(name='ceph')
    def ceph_group():
        """ Deploy and manage Ceph """
    ceph_group.add_command(ceph_ansible)
    return ceph_group


@click.command(name='ceph-ansible')
@click.option('--release', '-r', required=False, default=None,
              help='Ceph-Ansible stable release branch [optional]')
@click.option('--inventory', '-i', required=True,
              help='Ceph-Ansible inventory file path')
@click.option('--group-vars', '-g', 'group_vars', required=True,
              help='Ceph-Ansible grou_vars directory path')
@click.option('--ssh-key', '-s', 'ssh_key', required=True,
              help='Ceph-Ansible grou_vars directory path')
def ceph_ansible(release, inventory, group_vars, ssh_key):
    """ Run the Ceph-Ansible ansible-playbook command """
    if release is None:
        # Use the latest release when none are specified
        release = constants.CEPH_RELEASES[-1]
    ceph.ceph_ansible_exec(
        release=release,
        inventory_path=inventory,
        group_vars_path=group_vars,
        ssh_key_path=ssh_key)



# Deprecated
@click.command(name='gen-config')
def gen_config():
    """ Generates ceph configs in ansible container """
    cmd = ('ansible-playbook -e @/etc/breqwatr/cloud.yml -e '
           'ansible_connection=local -i localhost, '
           '/var/repos/bw-ansible/generate-ceph-config.yml')
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)


# Deprecated
@click.command(name='deploy')
def deploy():
    """ Deploy ceph on hosts """
    cmd = ('ansible-playbook -i /etc/breqwatr/ceph-inventory.yml '
           '/var/repos/ceph-ansible/site.yml')
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)


# Deprecated
@click.command(name='post-deploy')
def post_deploy():
    """ Creates ceph related file and pools """
    cmd = ('ansible-playbook -e @/etc/breqwatr/cloud.yml -i '
           '/etc/breqwatr/ceph-inventory.yml '
           '/var/repos/bw-ansible/ceph-post-deploy.yml')
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)


