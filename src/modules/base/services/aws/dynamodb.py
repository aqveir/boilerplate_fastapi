import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from botocore.exceptions import ClientError

from modules.base.config import config

dynamodb_resource = boto3.resource(
    "dynamodb", 
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)


# Get the service resource.
class DynamoDBService:

    def __init__(self, table_name: str = config.CLAIM_TABLE_NAME):
        self.dynamodb_connection = dynamodb_resource
        self.table_name = table_name
        self.dynamodb_table = self.dynamodb_connection.Table(self.table_name)

    
    def create_table(self, table_name, key_schema, attribute_definitions, provisioned_throughput):
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
        except Exception as e:
            print(f"Error creating table: {e}")
            return None

    
    def delete_table(self, table_name):
        """
        Delete a DynamoDB table.
        """
        try:
            response = self.dynamodb_connection.delete_table(TableName=table_name)
            return response
        except Exception as e:
            print(f"Error deleting table: {e}")
            return None
        
    
    """  Put an item in a DynamoDB table.

    This method is used to store data in a DynamoDB table. This method 
    takes a dictionary as input and stores it in the specified table.
    The dictionary should contain the attributes of the item to be 
    stored. The method returns the response from the DynamoDB service.

    If there is an error during the operation, it raises an exception.
    The exception can be caught and handled by the caller.
    """
    def set_data(self, data: dict):
        try:
            return self.dynamodb_table.put_item(
                Item=data
            )
        except Exception as e:
            raise e
        
    
    def get_data(self, value: str, key: str = config.CLAIM_TABLE_KEY):
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
            else:
                return None
        except Exception as e:
            print(f"Error getting item: {e}")
            return None


    def delete_data(self, value: str, key: str = config.CLAIM_TABLE_KEY):
        """
        Delete an item from a DynamoDB table.
        """
        try:
            response = self.dynamodb_table.delete_item(
                Key={key: value}
            )
            return response
        except Exception as e:
            print(f"Error deleting item: {e}")
            return None


    # Code referenced from
    # Link: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html#programming-with-python-documentation
    def dynamo_to_python(self, dynamo_object: dict) -> dict:
        deserializer = TypeDeserializer()
        return {
            k: deserializer.deserialize(v) 
            for k, v in dynamo_object.items()
        }
    def python_to_dynamo(self, python_object: dict) -> dict:
        serializer = TypeSerializer()
        return {
            k: serializer.serialize(v)
            for k, v in python_object.items()
        }