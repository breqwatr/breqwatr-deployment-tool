import sys
import os

import bwdt.lib.support as support

def is_aws_env_set():
    """ Return bool, are the AWS environment keys set? """
    return 'AWS_KEY_ID' in os.environ and 'AWS_KEY_SECRET' in os.environ


def keys():
    """ Return the AWS environment keys """
    return {
        'id': os.environ('AWS_KEY_ID'),
        'secret': os.environ('AWS_KEY_SECRET')}


def test_get_tunnel():
    assert is_aws_env_set(), 'env AWS_KEY_ID and AWS_KEY_SECRET must be set'
    tunnel = support.get_tunnel()
    print(tunnel)
    assert isinstance(tunnel, dict)
