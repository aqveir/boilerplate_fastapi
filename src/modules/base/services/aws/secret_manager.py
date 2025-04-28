""" Import the required modules """
import boto3
from botocore.exceptions import ClientError

from modules.base.config import config

client = boto3.client(
    "secretsmanager", 
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)

class SecretsManager:
    """ SecretsManager class to handle AWS Secrets Manager operations.

    This class is responsible for creating, deleting and retrieving secrets
    from AWS Secrets Manager. It uses the boto3 library to interact with
    AWS Secrets Manager.

    It is initialized with the secret name and the AWS Secrets Manager resource.
    The secret name is usually the name of the secret where the items will
    be stored. The AWS Secrets Manager resource is created using the boto3 library.
    """

    def __init__(self, secret_name: str = config.AWS_SECRET_NAME):
        self.client = client
        self.secret_name = secret_name


    def get(self, secret_name: str = config.AWS_SECRET_NAME) -> str:
        """
        Get a secret from AWS Secrets Manager.
        """
        try:
            response = self.client.get_secret_value(
                SecretId=secret_name
            )

            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary,
            # one of these fields will be populated
            if 'SecretString' in response:
                return response['SecretString']

            return response['SecretBinary']
        except ClientError as e:
            raise e
        except Exception as e:
            raise e
