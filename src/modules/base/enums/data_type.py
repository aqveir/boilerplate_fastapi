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
    LOOKUP = "data_type_lookup"
    LOCATION = "data_type_location"
    EXTERNAL = "data_type_external"
    FILE = "data_type_file"
    DATE = "data_type_date"
    DATETIME = "data_type_datetime"
    TIME = "data_type_time"
    EMAIL = "data_type_email"
    PHONE = "data_type_phone"
