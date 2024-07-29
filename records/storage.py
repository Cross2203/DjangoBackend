
from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Boto3Storage(S3Boto3Storage):
    def __init__(self, folder=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = folder