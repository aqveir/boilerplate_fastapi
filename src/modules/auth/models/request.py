import phonenumbers

from typing import Annotated, Union
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator, TypeAdapter, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

# Import configuration file
from modules.base.config import config

# MyNumberType = Annotated[ Union[str, PhoneNumber], PhoneNumberValidator() ] 
# USNumberType = Annotated[ Union[str, PhoneNumber], 
#                          PhoneNumberValidator(supported_regions=['US'], default_region='US', number_format=phonenumbers.PhoneNumberFormat.E164) 
#                         ]


class LoginRequest(BaseModel):
    username: EmailStr | str = Field(default=None, min_length=8, max_length=64, description="Username or Email or Phone Number")
    code: str | None = Field(default=None, min_length=4, max_length=64, description="Password or OTP")

    @model_validator(mode='after')
    def check_username(self) -> Self:
        # Check the username is for empty, email and phone number
        if '@' in self.username: # Email Validation
            ta_email = TypeAdapter(EmailStr)
            if not ta_email.validate(self.username):
                raise ValueError('Invalid email')
        elif self.username.isdigit(): # Phone Number Validation
            if len(self.username) < 10 :
                raise ValueError('Invalid phone number')
        else:
            raise ValueError('Invalid username')
        return self
    

class RegisterRequest(BaseModel):
    name: str = Field(default=None, min_length=2, max_length=64, description="Name")
    email: EmailStr= Field(..., description="Email", examples=["name@company.com"])
    phone_number: PhoneNumber | None = Field(default=None, description="Phone Number")

    @model_validator(mode='after')
    def check_email_domain(self) -> Self:
        # Check the email domain is allowed
        if self.email:
            email_domain = self.email.split('@')[1]
            if email_domain in config.RESTRICTED_DOMAINS:
                raise ValueError('Invalid email domain')
        return self