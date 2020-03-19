""" Controls for the apt service """
import bwdt.lib.docker as docker
from bwdt.constants import SERVICE_IMAGE_TAGS


def start(tag, port):
    """ Start the APT container """
    repo = 'apt'
    docker_kwargs = {
        'name': 'apt',
        'restart_policy': {'Name': 'always'},
        'ports': {'80': ('0.0.0.0', port)},
        'environment': {
            'GPG_PRIVATE_KEY_FILE': '/keys/breqwatr-private-key.asc',
            'GPG_PUBLIC_KEY_FILE': '/keys/breqwatr-private-key.asc'},
        'daemon': True
    }
    docker.get_image(repository=repo, tag=tag)
    docker.run(repo, tag, **docker_kwargs)
