from typing import Annotated, Self

from datetime import date
from pydantic import (
    ConfigDict, EmailStr, 
    Field, TypeAdapter, 
    computed_field, model_validator
)

# Import the project models
from modules.base.models.base import AppBaseModelWithHashAndAuditLog
from modules.core.models.organization.organization import Organization


class User(AppBaseModelWithHashAndAuditLog):
    """
    User model for the application.
    """
    title: str = Field(default=None, description="Title", exclude=True)
    first_name: str = Field(default=None, description="First Name",
            exclude=True, max_length=64, examples=["John"]
        )
    middle_name: str = Field(default=None, description="Middle Name",
            exclude=True
        )
    last_name: str = Field(default=None, description="Last Name",
            exclude=True, max_length=64, examples=["Doe"]
        )

    # Foreign Key to References
    organization: Organization = Field(default=None,
            description="Organization"
        )

    date_of_birth: date = Field(default=None,
            description="Date of Birth",
            exclude=True
        )

    username: EmailStr | str = Field(...,
            description="Username", max_length=64, min_length=8, 
            examples=["john@someone,com"]
        )

    is_verified: int = Field(default=0, description="Is Verified", exclude=True)


    def __str__(self):
        return f'User: {str(self.id)} - {self.full_name}'


    @computed_field(description="Full name")
    @property
    def full_name(self) -> str:
        """
        Get the full name of the user.
        The full name is a combination of the title, first name, middle name, and last name.
        """
        return_value: str = ""
        if self.title:
            return_value += f"{self.title} "

        if self.first_name:
            return_value += f"{self.first_name} "

        if self.middle_name:
            return_value += f"{self.middle_name} "

        if self.last_name:
            return_value += f"{self.last_name}"

        if len(return_value) < 1:
            return_value = "Unknown"

        return return_value.strip()


    @model_validator(mode='after')
    def check_username(self) -> Self:
        """
        Validate the username field.
        The username can be an email or a phone number.
        If the username is an email, it should be a valid email address.
        If the username is a phone number, it should be a valid phone number.
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


    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
        from_attributes=True
    )
