""" Import necessary modules """
from enum import Enum

# Define the Enum
class DataType(Enum):
    """
    DataType is an enumeration that defines the different types of Data Types.
    Each member of the enumeration represents a specific type.
    """
    STRING = "data_type_string"
    NUMBER = "data_type_number"
    BOOLEAN = "data_type_boolean"
    JSON = "data_type_json"
