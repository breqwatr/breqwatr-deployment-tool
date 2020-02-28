""" Module for interacting with AWS S3 """
# pylint: disable=import-error
import boto3

import bwdt.lib.license as license


class S3:
    """ Object class for S3 """
    def __init__(self):
        licensed, keys = license.keys()
        if licensed:
            session = boto3.Session(aws_access_key_id=keys['id'],
                                    aws_secret_access_key=keys['secret'])
        self.client = session.client('s3')

    def download(self, path, bucket_name, key):
        """ Download key from bucket_name to path """
        return self.client.download_file(bucket_name, key, path)

    def upload(self, path, bucket_name, key):
        """ Upload from path to bucket_name as key """
        return self.client.upload_file(path, bucket_name, key)
