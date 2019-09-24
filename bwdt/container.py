"""Container class for interacting with Docker """
import os
from base64 import b64decode

# pylint: disable=import-error
import boto3
import docker
from click import echo

import bwdt.auth as auth
from bwdt.envvar import env


class Docker(object):
    """Object to interact with docker & ECR"""
    def __init__(self):
        self.auth = auth.get()
        self._token = self._get_ecr_token()
        self._creds = self._get_docker_creds()
        self.client = self._get_docker_client()
        self.repo_prefix = self._get_repo_prefix()

    def _get_ecr_token(self):
        """ Return the token to auth to ECR """
        session = boto3.Session(
            aws_access_key_id=self.auth['key_id'],
            aws_secret_access_key=self.auth['key'])
        region = env()['region']
        client = session.client('ecr', region_name=region)
        return client.get_authorization_token()

    def _get_docker_creds(self):
        """Extract docker login credentials from an ECR token"""
        b64token = self._token['authorizationData'][0]['authorizationToken']
        decoded_token = b64decode(b64token)
        token_data = decoded_token.split(':')
        username = token_data[0]
        password = token_data[1]
        registry = self._token['authorizationData'][0]['proxyEndpoint']
        return {'username': username, 'password': password,
                'registry': registry}

    def _get_docker_client(self):
        """ Delete current login. Return an authenticated docker client """
        home = os.path.expanduser("~")
        docker_cred_path = '{}/.docker/config.json'.format(home)
        if os.path.exists(docker_cred_path):
            os.remove(docker_cred_path)
        client = docker.from_env()
        client.login(
            username=self._creds['username'],
            password=self._creds['password'],
            registry=self._creds['registry'])
        return client

    def _get_repo_prefix(self):
        """ Remove the protocol from registry cred to make the image prefix """
        prefix = self._creds['registry'].replace('https://', '')
        prefix = prefix.replace('http://', '')
        return prefix

    def pull(self, repository, tag, retag=True, remove_long=True):
        """ Pull an image from the registry """
        full_repo_name = "{}/{}".format(self.repo_prefix, repository)
        self.client.images.pull(repository=full_repo_name, tag=tag)
        if retag:
            self.tag(
                old_repo=full_repo_name,
                old_tag=tag,
                new_repo=repository,
                new_tag=tag)
            if remove_long:
                self.remove(repo=full_repo_name, tag=tag)

    def tag(self, old_repo, old_tag, new_repo, new_tag):
        """ docker tag """
        old_repo_full = '{}:{}'.format(old_repo, old_tag)
        image = self.client.images.get(old_repo_full)
        image.tag(new_repo, tag=new_tag)

    def remove(self, repo, tag):
        """ Docker rmi """
        image = '{}:{}'.format(repo, tag)
        self.client.images.remove(image=image)

    def retag(self, image_name, tag, new_registry_url):
        """ retag an upstream image to the new_registry_url """
        repository = '{}/{}:{}'.format(self.repo_prefix, image_name, tag)
        image = self.client.images.get(repository)
        new_repository = '{}/{}'.format(new_registry_url, image_name)
        image.tag(new_repository, tag=tag)

    def push(self, image_name, tag, registry_url):
        """ Push an image to a remote registry. Return true if success """
        repository = '{}/{}'.format(registry_url, image_name)
        result = self.client.images.push(repository, tag=tag)
        if 'gave HTTP response to HTTPS' in result:
            echo('ERROR: This registry is not HTTPS and not trusted')
            return False
        return True

    def list(self, **kwargs):
        """ List the running containers """
        if 'all' not in kwargs:
            kwargs['all'] = True
        return self.client.containers.list(**kwargs)

    def get_container(self, name):
        """ Return a container with matching name or None """
        containers = self.list()
        matches = [cntr for cntr in containers if cntr.name == name]
        if not matches:
            return None
        return matches[0]

    def run(self, image, name, **kwargs):
        """ Launch a docker container (noop if it already exists)

            Return True if launched, else False
        """
        if self.get_container(name):
            return False
        if 'detach' not in kwargs:
            kwargs['detach'] = True
        full_image = "{}/{}".format(self.repo_prefix, image)
        self.client.containers.run(full_image, name=name, **kwargs)
        return True

    def execute(self, container_name, cmd, silent=False):
        """ Run docker exec """
        if not silent:
            echo('{}> {}'.format(container_name, cmd))
        container = self.get_container(container_name)
        if not container:
            return {'exit_code': 1, 'output': 'Container not found'}
        exit_code, output = container.exec_run(cmd)
        return {'exit_code': exit_code, 'output': output}

    def export(self, image_name, tag, directory):
        """ Save a docker image from ECR to  directory """
        repository = '{}/{}:{}'.format(self.repo_prefix, image_name, tag)
        image = self.client.images.get(repository)
        filename_base = image_name.replace('/', '-')
        path = '{}/{}-{}.docker'.format(directory, filename_base, tag)
        with open(path, 'wb') as _file:
            for chunk in image.save(named=repository):
                _file.write(chunk)
