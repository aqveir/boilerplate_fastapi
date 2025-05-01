""" Import the required modules """
from typing_extensions import Self
from pydantic import (
    BaseModel, Field, model_validator, 
    TypeAdapter, EmailStr
)

# Import configuration file
from modules.base.config import config


class OrganizationBaseModel(BaseModel):
    """
    Base model for organization models.
    """
    display_name: str = Field(default=None, description="Display Name",
            max_length=128, examples=["My Organization"]
        )
    legal_name: str = Field(default=None, description="Legal Name",
            exclude=True, max_length=128,
            examples=["My Organization Inc"]
        )

    @model_validator(mode='after')
    def check_username(self) -> Self:
        """
        Validate the username field to check if it is a valid email or phone number.
        """
        # Check the username is for empty, email and phone number
        if '@' in self.username: # Email Validation
            ta_email = TypeAdapter(EmailStr)
            if not ta_email.validate_python(self.username):
                raise ValueError('Invalid email')
        elif str(self.username).isdigit(): # Phone Number Validation
            if len(self.username) < 10 :
                raise ValueError('Invalid phone number')
        else:
            raise ValueError('Invalid username')
        return self


# Define the Create model
class OrganizationCreateRequest(OrganizationBaseModel):
    """
    Model for organization create request.
    """
    pass

class OrganizationUpdateRequest(OrganizationBaseModel):
    """
    Model for organization update request.
    """
    pass
