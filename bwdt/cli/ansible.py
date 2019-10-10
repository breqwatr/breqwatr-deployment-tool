""" Commands for operating the Ansible service """
import click

import bwdt.services.ansible as ansible
import bwdt.cli.ceph
import bwdt.cli.openstack


@click.group(name='ansible')
def ansible_group():
    """ Command group for bwdt Ansible service """


@click.option('--ssh-key-path', required=True, help='path to SSH private key')
@click.option('--cloud-yml-path', required=True, help='path to cloud.yml file')
@click.option('--kolla-dir', required=False, default=None,
              help='optional mount path for kolla files')
@click.option('--ceph-dir', required=False, default=None,
              help='optional mount path for ceph files')
@click.command()
def start(ssh_key_path, cloud_yml_path, kolla_dir, ceph_dir):
    """Launch the local registry"""
    click.echo("Launching container: breqwatr/ansible")
    success = ansible.start(
        ssh_key_path=ssh_key_path,
        cloud_yml_path=cloud_yml_path,
        kolla_dir=kolla_dir,
        ceph_dir=ceph_dir)
    if success:
        click.echo('Done')
    else:
        click.echo('Failed to launch - Maybe its already running?')


@click.option('--server-ip', required=True, help='IP of compute node')
@click.option('--user', required=False, default='root',
              help='Optional username for SSH/SCP. Default: root')
@click.command(name='transfer-kolla-dir')
def transfer_kolla_dir(server_ip, user):
    """ Transfer the Ansible service's kolla dir to a compute node """
    txt = 'Transfering kolla to {}@{}:/etc/kolla'.format(server_ip, user)
    click.echo(txt)
    ansible.transfer_kolla_dir(server_ip, user=user)
    click.echo('Done')


ansible_group.add_command(transfer_kolla_dir)
ansible_group.add_command(start)
ansible_group.add_command(bwdt.cli.ceph.ceph_group)
ansible_group.add_command(bwdt.cli.openstack.openstack_group)
