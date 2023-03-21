import os

from storages.backends.s3boto3 import S3Boto3Storage


class MinIOStorage(S3Boto3Storage):
    print("MinIOStorage")
    bucket_name = 'storage-bucket'
    endpoint_url = f"http://{os.getenv('MINIO_URL')}:9000"
    access_key = os.environ.get('ACCESS_KEY')
    secret_key = os.environ.get('SECRET_KEY')
    region_name = 'us-west-2'
    default_acl = 'public-read'
    file_overwrite = False
