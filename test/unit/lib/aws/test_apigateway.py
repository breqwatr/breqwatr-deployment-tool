""" tests for api gateway """
import datetime
import bwdt.lib.aws.apigateway

def test_sign():
    """ get the keyed hash (hmac) of a msg as bytes"""
    result = bwdt.lib.aws.apigateway.sign(key=b'abc', msg='def')
    assert isinstance(result, bytes)


def test_get_signing_key():
    """ sign the arguments into eachother and return btes """
    time = datetime.datetime.utcnow()
    result = bwdt.lib.aws.apigateway.get_signing_key(
        secret_key='FAKE',
        time=time,
        region='ca-central-1')
    assert isinstance(result, bytes)


def test_get_amz_date():
    """ get a string from a timestamp """
    time = datetime.time(20, 2, 2, 376068)
    result = bwdt.lib.aws.apigateway.get_amz_date(time=time)
    assert isinstance(result, str)


def test_get_credential_scope():
    """ get a scope string given time and region """
    time = datetime.time(20, 2, 2, 376068)
    result = bwdt.lib.aws.apigateway.get_credential_scope(
        time=time,
        region='ca-central-1')
    assert isinstance(result, str)


def test_get_cannonical_request_digest():
    """ Return a cannonical request digest string """
    time = datetime.time(20, 2, 2, 376068)
    result = bwdt.lib.aws.apigateway.get_cannonical_request_digest(
        method='POST',
        host='abc.com',
        time=time,
        uri='/FAKE',
        body='EXAMPLE',
        query='?example=1')
    assert isinstance(result, str)


def test_get_signature():
    """ get a signature string """
    time = datetime.time(20, 2, 2, 376068)
    result = bwdt.lib.aws.apigateway.get_signature(
        secret_key='FAKE',
        time=time,
        region='ca-central-1',
        method='POST',
        host='example.com',
        body='',
        uri='/',
        query='?example=1')
    assert isinstance(result, str)


def test_get_authorization_header():
    """ get an auth header from args ... """
    time = datetime.datetime.utcnow()
    result = bwdt.lib.aws.apigateway.get_authorization_header(
        time=time,
        key_id='FAKE_ID',
        secret_key='FAKE KEY',
        region='ca-central-1',
        method='POST',
        host='example.com',
        body='bleh',
        uri='/',
        query='?whatever=1')

def test_get_headers():
    """ get headers ... """
    result = bwdt.lib.aws.apigateway.get_headers(
        key_id='A',
        secret_key='B',
        region='ca-central-1',
        method='POST',
        host='bleh.com',
        uri='/',
        query='?qwe=1',
        body='')
    assert isinstance(result, dict)
    assert 'Authorization' in result
    assert 'x-amz-date' in result
    assert 'x-amz-content-sha256' in result
