""" Controls for the Breqwatr services """

from bwdt.container import Docker


def registry_start(ip='0.0.0.0', port=5000):
    """ Start the registry container """
    repo = 'registry'
    tag = '2'
    image = '{}:{}'.format(repo, tag)
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    http_addr = "{}:{}".format(ip, port)
    env = {'REGISTRY_HTTP_ADDR': http_addr}
    success = docker.run(image, name='registry', environment=env)
    return success
