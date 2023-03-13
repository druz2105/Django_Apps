from storages.backends.s3boto3 import S3Boto3Storage


class MinIOStorage(S3Boto3Storage):
    print("MinIOStorage")
    bucket_name = 'storage-bucket'
    endpoint_url = 'http://localhost:9001'
    access_key = 'access-key'
    secret_key = 'secret-key'
    region_name = 'us-west-2'
    default_acl = 'public-read'
    file_overwrite = False
