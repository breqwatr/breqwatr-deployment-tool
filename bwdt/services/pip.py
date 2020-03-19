""" Controls for the pip service """
from bwdt.constants import SERVICE_IMAGE_TAGS
from bwdt.lib.container import Docker


def start(tag=None):
    """ Start the APT container """
    name = 'pip'
    repo = 'pip'
    tag = SERVICE_IMAGE_TAGS[repo]
    docker_kwargs = {
        'network_mode': 'host',
        'restart_policy': {'Name': 'always'}
    }
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    success = docker.run(repo, tag, name=name, **docker_kwargs)
    return success
