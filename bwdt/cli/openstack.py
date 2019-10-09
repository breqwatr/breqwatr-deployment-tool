""" Commands for operating the Ansible service """
import click


@click.group(name='openstack')
def openstack_group():
    """ Command group for bwdt ansible openstack """


@click.command(name='gen-config')
def gen_config():
    """ Generate OpenStack config files in the ansible container """
    cloud_yml = '-e @/etc/breqwatr/cloud.yml'
    conn = '-e ansible_connection=local'
    inv = '-i localhost,'
    playbook = '/var/repos/bw-ansible/generate-kolla-config.yml'
    cmd = 'ansible-playbook {} {} {} {}'.format(cloud_yml, conn, inv, playbook)
    docker_cmd = 'docker exec -it ansible {}'.format(cmd)
    click.echo(docker_cmd)


@click.command()
def bootstrap():
    """ Run kolla-ansible bootstrap """
    cmd = ('docker exec -it ansible kolla-ansible'
           '-i /etc/kolla/inventory bootstrap-servers')
    click.echo(cmd)


@click.command()
def deploy():
    """ Run kolla-ansible deploy """
    cmd = ('docker exec -it ansible kolla-ansible'
           '-i /etc/kolla/inventory deploy')
    click.echo(cmd)


@click.command(name='post-deploy')
def post_deploy():
    """ Run kolla-ansible post-deploy """
    cmd = ('docker exec -it ansible kolla-ansible'
           '-i /etc/kolla/inventory post-deploy')
    click.echo(cmd)


openstack_group.add_command(gen_config)
openstack_group.add_command(bootstrap)
openstack_group.add_command(deploy)
openstack_group.add_command(post_deploy)
