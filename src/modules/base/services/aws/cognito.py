""" Import the required modules """
from typing import Optional, Tuple
import boto3
from modules.base.config import config

client = boto3.client(
    "elasticache", 
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)


class Cognito():
    """
    Memcached cache backend implementation using AWS ElastiCache.

    This class implements the ICache interface and provides methods to 
    interact with a Memcached cache.
    It uses the AWS SDK for Python (Boto3) to interact with AWS ElastiCache.
    """
    def __init__(self):
        self.client = client


    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:
        return 3600, await self.get(key)


    async def get(self, key: str) -> Optional[bytes]:
        return await self.client.get(key)


    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:
        await self.client.set(key, value, exptime=expire or 0)


    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        raise NotImplementedError
