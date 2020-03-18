""" Controls for the apt service """
import bwdt.lib.docker as docker
from bwdt.constants import SERVICE_IMAGE_TAGS


def start(tag, port):
    """ Start the APT container """
    name = 'apt'
    repo = 'apt'
    image = '{}:{}'.format(repo, tag)
    restart_policy = {'Name': 'always'}
    env = {
        'GPG_PRIVATE_KEY_FILE': '/keys/breqwatr-private-key.asc',
        'GPG_PUBLIC_KEY_FILE': '/keys/breqwatr-private-key.asc',
    }
    ports = {'80': ('0.0.0.0', port)}
    docker.get_image(repository=repo, tag=tag)
    success = docker.run(repo, tag, name=name, environment=env, daemon=True,
                         restart_policy=restart_policy, ports=ports)
    return success
