""" Commands for setting up ceph """

import click


@click.group(name='ceph')
def ceph_group():
    """ Command group for ceph """


@click.command(name='gen-config')
def gen_config():
    """ Generates ceph configs in ansible container """
    cmd = ('ansible-playbook -e @/etc/breqwatr/cloud.yml -e '
           'ansible_connection=local -i localhost, '
           '/var/repos/bw-ansible/generate-ceph-config.yml')
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)


@click.command(name='deploy')
def deploy():
    """ Deploy ceph on hosts """
    cmd = ('ansible-playbook -i /etc/breqwatr/ceph-inventory.yml '
           '/var/repos/ceph-ansible/site.yml')
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)


@click.command(name='post-deploy')
def post_deploy():
    """ Creates ceph related file and pools """
    cmd = ('ansible-playbook -e @/etc/breqwatr/cloud.yml -i '
           '/etc/breqwatr/ceph-inventory.yml '
           '/var/repos/bw-ansible/ceph-post-deploy.yml')
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)

ceph_group.add_command(deploy)
ceph_group.add_command(gen_config)
ceph_group.add_command(post_deploy)
