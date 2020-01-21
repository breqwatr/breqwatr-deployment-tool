""" Interact with AWS API Gateway """
import datetime
import hashlib
import hmac
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


def get_cannonical_request_digest(method, host, time, body, uri, query):
    """ return digest of a cannonical request string """
    amzdate = get_amz_date(time)
    canonical_headers = (
        f'host:{host}\n'
        f'x-amz-date:{amzdate}\n')
    signed_headers = 'host;x-amz-date'
    payload_hash = get_payload_hash(body)
    can_req = (
        f'{method}\n'
        f'{uri}\n'
        f'{query}\n'
        f'{canonical_headers}\n'
        f'{signed_headers}\n'
        f'{payload_hash}')
    return hashlib.sha256(can_req.encode('utf-8')).hexdigest()


def get_signature(secret_key, time, region, method, host, body, uri, query):
    """ Return signature for aws header """
    sig_key = get_signing_key(secret_key, time, region)
    amzdate = get_amz_date(time)
    cred_scope = get_credential_scope(time, region)
    req_digest = get_cannonical_request_digest(
        method=method,
        host=host,
        time=time,
        body=body,
        uri=uri,
        query=query)
    sign_str = (
        f'AWS4-HMAC-SHA256\n'
        f'{amzdate}\n'
        f'{cred_scope}\n'
        f'{req_digest}')
    sign_str_utf8 = sign_str.encode('utf-8')
    algorithm = hashlib.sha256
    sig_hmac = hmac.new(sig_key, sign_str_utf8, algorithm)
    return sig_hmac.hexdigest()


def get_authorization_header(time, key_id, secret_key, region, method, host, body, uri, query):
    """ Return an aws authorization header """
    credential_scope = get_credential_scope(time, region)
    signature = get_signature(
        secret_key=secret_key,
        time=time,
        region=region,
        method=method,
        host=host,
        body=body,
        uri=uri,
        query=query)
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
    headers = {
        'Authorization': authorization,
        'x-amz-date': get_amz_date(time),
        'x-amz-content-sha256': get_payload_hash(body)}
    return headers


def post(key_id, secret_key, region, host, body, uri, query):
    """ do a request - needs some work"""
    headers = get_headers(key_id, secret_key, region, 'POST', host, body, uri,
                          query)
    url = f'https://{host}{uri}'
    payload = {}
    return requests.post(url, headers=headers, data=payload)

