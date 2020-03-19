""" Controls for the pip service """
from bwdt.constants import SERVICE_IMAGE_TAGS
import bwdt.lib.docker as docker


def start(tag=None):
    """ Start the APT container """
    repo = 'pip'
    docker_kwargs = {
        'name': 'pip',
        'network_mode': 'host',
        'restart_policy': {'Name': 'always'},
        'daemon': True
    }
    docker.get_image(repo, tag)
    docker.run(repo, tag, name=name, **docker_kwargs)
