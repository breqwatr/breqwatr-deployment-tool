""" Controls for the registry service """
from bwdt.constants import SERVICE_IMAGE_TAGS
from bwdt.container import Docker


def start(ip='0.0.0.0', port=5000):
    """ Start the registry container """
    name = 'registry'
    repo = 'registry'
    tag = SERVICE_IMAGE_TAGS[repo]
    http_addr = "{}:{}".format(ip, port)
    image = '{}:{}'.format(repo, tag)
    docker_kwargs = {
        'environment': {'REGISTRY_HTTP_ADDR': http_addr},
        'ports': {'5000': '5000'}
    }
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    success = docker.run(image, name=name, **docker_kwargs)
    return success


# def online_sync_img(image, local_registry, port=5000, silent=False, tag=TAG):
#     """ Pull image from upstream,push to local registry """
#    if not silent:
#         print('Pulling from upstream repo: {}'.format(image))


# def registry_sync(local_registry, port=5000, silent=False):
#     """ Pull images from upstream or import from media, push to registry """
#     # for image in IMAGES:
#     # docker = Docker()
