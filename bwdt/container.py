"""Container class for interacting with Docker """
import json
import os
from base64 import b64decode

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
        """Returns an authenticated docker client"""
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

    def pull(self, repository, tag):
        """ Pull an image from the registry """
        full_repo_name = "{}/{}".format(self.repo_prefix, repository)
        self.client.images.pull(repository=full_repo_name, tag=tag)

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
