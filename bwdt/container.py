"""Container class for interacting with Docker """
import json
from base64 import b64decode

import boto3
import docker

import bwdt.lib as lib


class Docker(object):
    """Object to interact with docker & ECR"""
    def __init__(self):
        with open(lib.env()['auth_file'], 'r') as auth_file:
            self.auth = json.load(auth_file)
        self.token = self._get_ecr_token()
        self.creds = self._get_docker_creds()
        self.client = self._get_docker_client()
        self.repo_prefix = self._get_repo_prefix()

    def _get_ecr_token(self):
        """ Return the token to auth to ECR """
        session = boto3.Session(
            aws_access_key_id=self.auth['key_id'],
            aws_secret_access_key=self.auth['key'])
        client = session.client('ecr', region_name=lib.env()['region'])
        return client.get_authorization_token()

    def _get_docker_creds(self):
        """Extract docker login credentials from an ECR token"""
        b64token = self.token['authorizationData'][0]['authorizationToken']
        decoded_token = b64decode(b64token)
        token_data = decoded_token.split(':')
        username = token_data[0]
        password = token_data[1]
        registry = self.token['authorizationData'][0]['proxyEndpoint']
        return {'username': username, 'password': password,
                'registry': registry}

    def _get_docker_client(self):
        """Returns an authenticated docker client"""
        client = docker.from_env()
        client.login(**self.creds)
        return client

    def _get_repo_prefix(self):
        """ Remove the protocol from registry cred to make the image prefix """
        prefix = self.creds['registry'].replace('https://', '')
        prefix = prefix.replace('http://', '')
        return prefix

    def pull(self, repository, tag):
        """ Pull an image from the registry """
        full_repo_name = "{}/{}".format(self.repo_prefix, repository)
        self.client.images.pull(repository=full_repo_name, tag=tag)

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
        """ Launch a docker container (noop if it already exists)i
            Return True if launched, else False
        """
        if self.get_container(name):
            return False
        if 'detach' not in kwargs:
            kwargs['detach'] = True
        full_image = "{}/{}".format(self.repo_prefix, image)
        self.client.containers.run(full_image, name=name, **kwargs)
        return True
