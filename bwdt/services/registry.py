""" Controls for the registry service """
from click import echo
from bwdt.constants import KOLLA_IMAGE_TAGS, SERVICE_IMAGE_TAGS
from bwdt.container import Docker, get_auth


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


def _offline_sync_image(registry_url, image, tag):
    """ Import image and push to local registry """
    echo('> Importing {}:{}'.format(image, tag))
    echo('> Pushing {}:{} to {}'.format(image, tag, registry_url))
    raise Exception('Offline is not supported yet')


def _online_sync_image(registry_url, image, tag):
    """ Pull image from upstream,push to local registry """
    echo('> Pulling image: {}:{}'.format(image, tag))
    docker = Docker()
    docker.pull(image, tag)
    echo('> Applying new tag')
    docker.retag(image, tag, registry_url)
    echo('Pushing {}:{} to {}'.format(image, tag, registry_url))
    docker.push(image, tag, registry_url)


def sync_image(registry_url, image, tag=None):
    """ Pull images from upstream or import from media, push to registry """
    if tag is None:
        tag = KOLLA_IMAGE_TAGS[image]
    auth = get_auth()
    offline_str = str(auth['offline']).lower()
    if offline_str == "true":
        _offline_sync_image(registry_url, image, tag)
    else:
        _online_sync_image(registry_url, image, tag)


def sync_all_images(registry_url, tag=None):
    """ Sync all images to registry_url """
    for image in KOLLA_IMAGE_TAGS:
        sync_image(registry_url, image, tag)
