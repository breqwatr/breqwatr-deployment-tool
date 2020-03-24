""" Docker shell command runner - the docker python lib isn't worth using """
import subprocess
import sys

import bwdt.lib.config as config
import bwdt.constants as constants
import bwdt.lib.aws.ecr as ecr
from bwdt.lib.envvar import env


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


def is_image_pulled(repository, tag):
    """ Return True if image is pulled, else False """
    prefix = constants.IMAGE_PREFIX
    cmd = f'docker image inspect {prefix}/{repository}:{tag}'.split(' ')
    try:
        subprocess.check_call(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def assert_image_pulled(repository, tag):
    """ Gracefully exit if a required docker image is not present """
    if not is_image_pulled(repository, tag):
        err = f'ERROR: The requested image {repository}:{tag} was not found!\n'
        sys.stderr.write(err)
        sys.exit(1)


def assert_valid_release(release):
    """ Gracefully exist it an invalid release is requested """
    if release not in constants.RELEASES:
        err = (f'ERROR: Release "{release}" is not supported.\n'
               f'       Supported releases: {constants.RELEASES}\n')
        sys.stderr.write(err)
        sys.exit(1)


def shell(cmd):
    """ Run the given command """
    if env()['BWDT_DEBUG'] != 'false':
        print(cmd)
    if env()['BWDT_DISABLE_SHELL'] == 'false':
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as error:
            sys.stderr.write(f'\n\n{error}\n')
            sys.exit(1)


def _default_tag(repository):
    """ Return the default tag when not specified """
    tags = {}
    tags.update(constants.SERVICE_IMAGE_TAGS)
    tags.update(constants.KOLLA_IMAGE_TAGS)
    if repository not in tags:
        err = f'ERROR: Repository {repository} has no default tag defined.\n'
        sys.stderr.write(err)
        sys.exit(1)
    return tags[repository]


def load(repository, tag):
    """ Import an image from the offline_path """
    assert_installed()
    raise NotImplementedError
    # cmd = f'docker load --input {path}'
    # shell(cmd)


def apply_tag(old_tag, new_tag):
    """ Apply a docker tag to an image """
    assert_installed()
    cmd = f'docker tag {old_tag} {new_tag}'
    shell(cmd)


def delete_image(image):
    """ Delete the given image, or its tag if it has more than one tag """
    assert_installed()
    cmd = f'docker image img {image}'
    shell(cmd)


def pull_ecr(repository, tag):
    """ Pull an image from ECR. Retag to DHUB name and delete the old one.  """
    assert_installed()
    ecr_url = ecr.get_ecr_url()
    image = f'{ecr_url}/{constants.IMAGE_PREFIX}/{repository}:{tag}'
    cmd = f'docker pull {image}'
    shell(cmd)
    new_tag = f'{constants.IMAGE_PREFIX}/{repository}:{tag}'
    apply_tag(image, new_tag)
    delete_image(image)


def pull_dhub(repository, tag):
    """ Pull an image from Docker Hub """
    assert_installed()
    cmd = f'docker pull {constants.IMAGE_PREFIX}/{repository}:{tag}'
    shell(cmd)


def get_image(repository, tag=None, overwrite=True):
    """ Pull or load given docker image.

        If config is set to offline mode, import it from the offline_path
        If use_ecr is False or is_licensed is False, pull from Docker Hub
        If use_ecr is True and is_licensed is True, pull from ECR
        If overwrite is False and the image exists, do nothing
    """
    if tag is None:
        tag = _default_tag(repository)
    if is_image_pulled(repository, tag) and not overwrite:
        return
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


def run(repository, tag, **kwargs):
    """ Run a docker image

        Wraps the docker run command.
        Tries to use the same contract as the python docker library.

        Keyword Arguments:
            daemon:         -d
            name:           --name
            restart_policy: --restart
            ports:          -p
            environment:    -e
            network_mode:   --network

    """
    assert_installed()
    if tag is None:
        tag = _default_tag(repository)
    image = f'{repository}:{tag}'
    cmd = 'docker run'
    if 'daemon' in kwargs and kwargs['daemon']:
        cmd += ' -d'
    if 'name' in kwargs:
        name = kwargs['name']
        cmd += f' --name {name}'
        # Also remove any present containers with this name
        rm_cmd = f'docker rm -f {name} 2> /dev/null || true'
        shell(rm_cmd)
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
    if 'network_mode' in kwargs:
        network_mode = kwargs['network_mode']
        cmd += f' --network {network_mode}'
    cmd += f' {constants.IMAGE_PREFIX}/{image}'
    shell(cmd)


def push(image):
    """ Push a docker image """
    cmd = f'docker push {image}'
    shell(cmd)
