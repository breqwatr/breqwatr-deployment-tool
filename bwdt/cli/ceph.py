""" Commands for setting up ceph """

import click


@click.group(name='ceph')
def ceph_group():
    """ Command group for ceph """


@click.command(name='gen-config')
def gen_config():
    """ Generates ceph configs in ansible container """
    click.echo("Generating ceph config files")
    cmd = ('ansible-playbook -e @/etc/breqwatr/cloud.yml -e '
          'ansible_connection=local -i localhost, '
          '/var/repos/bw-ansible/generate-ceph-config.yml')
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)

ceph_group.add_command(gen_config)
