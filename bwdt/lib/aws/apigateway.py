""" Interact with AWS API Gateway """
import datetime
import hashlib
import hmac
import json
import requests


def sign(key, msg):
    """
        Return bytes - sha256 keyed hash of msg
        key: bytes representing singing key
        msg: string representing message to be hashed
    """
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signing_key(secret_key, time, region):
    # see https://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
    """
        *All hashes use sha256 on utf-8 strings*
        - Using 'AWS4' as the crypto-key, hash your secret key
        - Using the hmac of your secret key, hash the current datestamp
        - Using the hmac of the date, hash your region
        - Using the hmac of your region, hash the service name
        - Using the hmac of your service, hash 'aws4_request'
        Return this hmac to use as a singing key against your message body
    """
    datestamp = time.strftime('%Y%m%d')
    aws4_header_bytes = ('AWS4' + secret_key).encode('utf-8')
    key_date = sign(aws4_header_bytes, datestamp)
    key_region = sign(key_date, region)
    key_service = sign(key_region, 'execute-api')
    key_aws4_request = sign(key_service, 'aws4_request')
    return key_aws4_request


def get_amz_date(time):
    """ Get a timestamp string in the format of the amz-date header """
    return time.strftime('%Y%m%dT%H%M%SZ')


def get_credential_scope(time, region):
    """ Return the scope string for a credential """
    datestamp = time.strftime('%Y%m%d')
    return f'{datestamp}/{region}/execute-api/aws4_request'


def get_payload_hash(body):
    """ Return a hash of the request payload """
    body = body.encode('utf-8')
    return hashlib.sha256(body).hexdigest()


def get_canonical_headers(host, time):
    """ Return the canonical headers """
    amzdate = get_amz_date(time)
    return (
        f'host:{host}\n'
        f'x-amz-date:{amzdate}\n')


def get_canonical_request(method, uri, query, canonical_headers, payload_hash):
    """ return digest of a canonical request string """
    # https://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
    signed_headers = 'host;x-amz-date'
    return (
        f'{method}\n'
        f'{uri}\n'
        f'{query}\n'
        f'{canonical_headers}\n'
        'host;x-amz-date\n'
        f'{payload_hash}')


def get_string_to_sign(time, credential_scope, canonical_request_digest):
    """ Returnt the AWS String-to-sign in utf-8 """
    # https://docs.aws.amazon.com/general/latest/gr/sigv4-create-string-to-sign.html
    amzdate = get_amz_date(time)
    return (
        f'AWS4-HMAC-SHA256\n'
        f'{amzdate}\n'
        f'{credential_scope}\n'
        f'{canonical_request_digest}')


def get_signature(signing_key, string_to_sign):
    """ Return hexdigest of signature for aws header """
    sts_utf8 = string_to_sign.encode('utf-8')
    sig = hmac.new(signing_key, sts_utf8, hashlib.sha256)
    return sig.hexdigest()


def get_authorization_header(time, key_id, secret_key, region, method, host,
                             body, uri, query):
    """ Return an aws authorization header """
    # canonical request is a multi-line string with a particular format
    canonical_headers = get_canonical_headers(host, time)
    payload_hash = get_payload_hash(body)
    canonical_request = get_canonical_request(
         method=method,
         uri=uri,
         query=query,
         canonical_headers=canonical_headers,
         payload_hash=payload_hash)
    # create a string-to-sign from the canonical requests' digest
    cr_digest = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    credential_scope = get_credential_scope(time, region)
    string_to_sign = get_string_to_sign(time, credential_scope, cr_digest)
    # sign the String-To-Sign with a signing key derived from secret iam key
    signing_key = get_signing_key(secret_key, time, region)
    signature = get_signature(signing_key, string_to_sign)
    # return the headers all in one string
    return (
        f'AWS4-HMAC-SHA256 Credential={key_id}/{credential_scope}, '
        f'SignedHeaders=host;x-amz-date, '
        f'Signature={signature}')


def get_headers(key_id, secret_key, region, method, host, body, uri, query):
    """ Return the headers required for AWS API Gateway requests """
    time = datetime.datetime.utcnow()
    authorization = get_authorization_header(
        time=time,
        key_id=key_id,
        secret_key=secret_key,
        region=region,
        method=method,
        host=host,
        body=body,
        uri=uri,
        query=query)
    amz_date = get_amz_date(time)
    payload_hash = get_payload_hash(body)
    return {
        'Authorization': authorization,
        'x-amz-date': amz_date,
        'x-amz-content-sha256': payload_hash}


def post(key_id, secret_key, region, host, uri, query, body=''):
    """ Execute a POST request """
    body_str = json.dumps(body)
    headers = get_headers(
        key_id=key_id,
        secret_key=secret_key,
        region=region,
        method='POST',
        host=host,
        body=body_str,
        uri=uri,
        query='')
    url = f'https://{host}{uri}'
    return requests.post(url, headers=headers, json=body)


def get(key_id, secret_key, region, host, uri, query):
    """ Execute a GET request """
    body_str = ''
    headers = get_headers(
        key_id=key_id,
        secret_key=secret_key,
        region=region,
        method='GET',
        host=host,
        body=body_str,
        uri=uri,
        query='')
    url = f'https://{host}{uri}'
    return requests.get(url, headers=headers)
