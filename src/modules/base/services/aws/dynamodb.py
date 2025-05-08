""" Import the required modules """
from typing import List
import boto3
from boto3.dynamodb.conditions import Key
# from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from botocore.exceptions import ClientError
from modules.base.exceptions.base import (
    AWSValueException
)

from modules.base.config import config

dynamodb_resource = boto3.resource(
    "dynamodb", 
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)


# Get the service resource.
class DynamoDBService:
    """ DynamoDBService class to handle DynamoDB operations.

    This class is responsible for creating, deleting and retrieving items
    from a DynamoDB table. It uses the boto3 library to interact with
    DynamoDB.

    It is initialized with the table name and the DynamoDB resource.
    The table name is usually the name of the table where the items will
    be stored. The DynamoDB resource is created using the boto3 library.
    """

    def __init__(self, table_name: str = config.CLAIM_TABLE_NAME):
        self.dynamodb_connection = dynamodb_resource
        self.table_name = table_name
        self.dynamodb_table = self.dynamodb_connection.Table(self.table_name)


    def create_table(self, table_name, key_schema,
            attribute_definitions, provisioned_throughput
        ):
        """
        Create a DynamoDB table.
        """
        try:
            response = self.dynamodb_connection.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput=provisioned_throughput
            )
            return response
        except ClientError as e:
            raise AWSValueException(exception=e) from e


    def delete_table(self, table_name):
        """
        Delete a DynamoDB table.
        """
        try:
            response = self.dynamodb_connection.delete_table(TableName=table_name)
            return response
        except ClientError as e:
            raise AWSValueException(exception=e) from e


    def set_data(self, data: dict) -> dict:
        """  Put an item in a DynamoDB table.

        This method is used to store data in a DynamoDB table. This method 
        takes a dictionary as input and stores it in the specified table.
        The dictionary should contain the attributes of the item to be 
        stored. The method returns the response from the DynamoDB service.

        If there is an error during the operation, it raises an exception.
        The exception can be caught and handled by the caller.
        """
        try:
            return self.dynamodb_table.put_item(
                Item=data
            )
        except ClientError as e:
            raise AWSValueException(exception=e) from e


    def get_data(self, value: str,
            key:str = config.CLAIM_TABLE_KEY
        ) -> dict | None:
        """
        Get an item from a DynamoDB table.
        """
        try:
            # Get the item from the table using the key
            response = self.dynamodb_table.get_item(
                Key={key: value}
            )

            # Check if the item exists in the response
            if 'Item' in response:
                return response['Item']

            return None
        except ClientError as e:
            raise AWSValueException(exception=e) from e


    def query_data(self, query: dict[str, str]) -> List[str] | None:
        """
        Get an item from a DynamoDB table.
        """
        try:
            keys: List[str] = list(query.keys())

            # Get the item from the table using the key
            response = self.dynamodb_table.query(
                KeyConditionExpression=Key(keys[0]).eq(query[0])
            )

            # Check if the item exists in the response
            if 'Items' in response:
                return str(response['Items'])

            return None
        except ClientError as e:
            raise AWSValueException(exception=e) from e


    def delete_data(self, value: str, key: str = config.CLAIM_TABLE_KEY):
        """
        Delete an item from a DynamoDB table.
        """
        try:
            response = self.dynamodb_table.delete_item(
                Key={key: value}
            )
            return response
        
        except ClientError as e:
            raise AWSValueException(exception=e) from e


    # Code referenced from
    # Link: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html#programming-with-python-documentation
    # def dynamo_to_python(self, dynamo_object: dict) -> dict:
    #     deserializer = TypeDeserializer()
    #     return {
    #         k: deserializer.deserialize(v) 
    #         for k, v in dynamo_object.items()
    #     }
    # def python_to_dynamo(self, python_object: dict) -> dict:
    #     serializer = TypeSerializer()
    #     return {
    #         k: serializer.serialize(v)
    #         for k, v in python_object.items()
    #     }
