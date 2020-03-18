""" Docker shell command runner - the docker python lib isn't worth using """
import subprocess
import sys

import bwdt.lib.config as config
import bwdt.lib.aws.ecr as ecr
from bwdt.lib.envvar import env
from bwdt.constants import IMAGE_PREFIX, SERVICE_IMAGE_TAGS, KOLLA_IMAGE_TAGS


def assert_installed():
    """ Return if Docker appears to be installed or not """
    out = subprocess.Popen(
        ['which', 'docker'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout = out.communicate()[0]
    is_installed = stdout != b''
    if not is_installed:
        err = 'ERROR: Docker does not apppear to be installed\n'
        sys.stderr.write(err)
        sys.exit(1)


def shell(cmd):
    """ Run the given command """
    if env()['BWDT_DEBUG'] != 'false':
        print(cmd)
    if env()['BWDT_DISABLE_SHELL'] == 'false':
        subprocess.check_call(cmd, shell=True)


def _default_tag(repository):
    """ Return the default tag when not specified """
    tags = {}
    tags.update(SERVICE_IMAGE_TAGS)
    tags.update(KOLLA_IMAGE_TAGS)
    if repository not in tags:
        err = f'ERROR: Repository {repository} has no default tag defined.\n'
        sys.stderr.write(err)
        sys.exit(1)
    return tags[repository]


def load(repository, tag):
    """ Import an image from the offline_path """
    assert_installed()
    cmd = f'docker load --input {path}'
    shell(cmd)


def tag(old_tag, new_tag):
    """ Apply a docker tag to an image """
    assert_installed()
    cmd = f'docker tag {old_tag} {new_tag}'


def delete_image(image):
    """ Delete the given image, or its tag if it has more than one tag """
    assert_installed()
    cmd = f'docker image img {image}'
    shell(cmd)


def pull_ecr(repository, tag):
    """ Pull an image from ECR. Retag to DHUB name and delete the old one."""
    assert_installed()
    ecr_url = ecr.get_ecr_url()
    image = f'{ecr_url}/{IMAGE_PREFIX}/{repository}:{tag}'
    cmd = f'docker pull {image}'
    shell(cmd)
    new_tag = f'{IMAGE_PREFIX}/{repository}:{tag}'
    tag(image, new_tag)
    delete(image)


def pull_dhub(repository, tag):
    """ Pull an image from Docker Hub """
    assert_installed()
    cmd = f'docker pull {IMAGE_PREFIX}/{repository}:{tag}'
    shell(cmd)


def get_image(repository, tag=None):
    """ Pull or load given docker image.

        If config is set to offline mode, import it from the offline_path
        If use_ecr is False or is_licensed is False, pull from Docker Hub
        If use_ecr is True and is_licensed is True, pull from ECR
    """
    if tag is None:
        tag = _default_tag(repository)
    # Handle offline mode
    if config.is_offline():
        load(repository, tag)
    else:
        dhub_override = False
        use_ecr = (config.is_licensed() and not dhub_override)
        if use_ecr:
            pull_ecr(repository, tag)
        else:
            pull_dhub(repository, tag)


def run(image, **kwargs):
    """ Run a docker image

        Wraps the docker run command.
        Tries to use the same contract as the python docker library.

        Keyword Arguments:
            daemon:         -d
            name:           --name
            restart_policy: --restart
            ports:          -p
            environment:    -e

    """
    assert_installed()
    cmd = 'docker run'
    if 'daemon' in kwargs and kwargs['daemon']:
        cmd += ' -d'
    if 'name' in kwargs:
        name = kwargs['name']
        cmd += f' --name {name}'
    if 'restart_policy' in kwargs:
        policy = kwargs['restart_policy']['Name']
        cmd += f' --restart {policy}'
    if 'ports' in kwargs:
        for container_port in kwargs['ports']:
            target = kwargs['ports'][container_port]
            if isinstance(target, tuple):
                host_ip = target[0]
                host_port = target[1]
                cmd += f' -p {host_ip}:{host_port}:{container_port}'
            else:
                host_port = target
                cmd += f' -p {host_port}:{container_port}'
    if 'environment' in kwargs:
        for key in kwargs['environment']:
            value = kwargs['environment'][key]
            cmd += f' -e {key}="{value}"'
    cmd += f' {IMAGE_PREFIX}/{image}'
    shell(cmd)
