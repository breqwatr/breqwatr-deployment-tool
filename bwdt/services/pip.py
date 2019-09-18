""" Controls for the pip service """
from bwdt.constants import SERVICE_IMAGE_TAGS
from bwdt.container import Docker


def start(tag=None):
    """ Start the PIP container """
    repo = 'pip'
    tag = SERVICE_IMAGE_TAGS[repo]
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    image = '{}:{}'.format(repo, tag)
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    docker.run(image, name='bw-pip', network_mode='host')
