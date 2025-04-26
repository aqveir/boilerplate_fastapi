import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from botocore.exceptions import ClientError

from modules.base.config import config

s3_resource = boto3.resource(
    "s3", 
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)

class SimpleStorageService:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.service_connection = s3_resource
        self.s3_bucket = self.service_connection.Bucket(self.bucket_name)

    def put(self, file_path: str, object_name: str):
        # Logic to upload a file to S3
        pass

    def get(self, object_name: str, file_path: str):
        # Logic to download a file from S3
        pass

    def delete(self, object_name: str):
        # Logic to delete a file from S3
        pass

    def list(self, prefix: str = ''):
        # Logic to list files in S3 bucket
        pass