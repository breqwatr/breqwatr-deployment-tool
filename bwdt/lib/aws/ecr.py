""" Module for interacting with AWS ECR """
import sys
from base64 import b64decode

# pylint: disable=import-error
import boto3
import botocore.exceptions

import bwdt.lib.license as license
from bwdt.lib.envvar import env


def get_ecr_client():
    """ Return an ECR boto3 client """
    licensed, keys = license.keys()
    if licensed:
        session = boto3.Session(aws_access_key_id=keys['id'],
                                aws_secret_access_key=keys['secret'])
    region = env()['BWDT_AWS_REGION']
    client = session.client('ecr', region_name=region)
    return client


def get_ecr_token():
    """ Get token or fail gracefully """
    client = get_ecr_client()
    try:
        token = client.get_authorization_token()
    except botocore.exceptions.ClientError:
        err = 'ERROR: Failed connecting to registry (invalid key)\n'
        sys.stderr.write(err)
        sys.exit(1)
    return token


def get_ecr_credentials(token):
    """ decode and parse ECR token into usable dict """
    b64token = token['authorizationData'][0]['authorizationToken']
    decoded_token = b64decode(b64token)
    token_data = decoded_token.decode("utf-8").split(':')
    username = token_data[0]
    password = token_data[1]
    registry = token['authorizationData'][0]['proxyEndpoint']
    credentials = {
        'username': username,
        'password': password,
        'registry': registry}
    return credentials


def get_registry_url(credentials):
    """ Given credentials dict, return the registry URL """
    registry = credentials['registry']
    url = registry.replace('https://', '')
    url = url.replace('http://', '')
    return url
