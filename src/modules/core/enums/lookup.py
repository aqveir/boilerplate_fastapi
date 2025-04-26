""" Import necessary modules """
from enum import Enum

# Define the Enum
class LookupMaster(Enum):
    """
    LookupMaster is an enumeration that defines the different types of lookup masters.
    Each member of the enumeration represents a specific type of lookup master.
    """
    ORGANIZATION_TYPE = "organization_type"
    USER_TYPE = "user_type"
    USER_STATUS = "user_status"
