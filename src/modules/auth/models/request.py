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


class UserNameModel(BaseModel):
    """
    Base model for username based requests.
    """
    username: str = Field(..., min_length=8, max_length=64,
        description="Username or Email or Phone Number",
        examples=["me@yourcompany.com", "+14155552671"])

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


class PasswordModel(BaseModel):
    """
    Base model for password based requests.
    """
    new_password: str = Field(..., min_length=8, max_length=64,
            description="New Password"
        )
    confirm_password: str = Field(..., min_length=8, max_length=64,
            description="Confirm Password"
        )

    @model_validator(mode='after')
    def check_password(self) -> Self:
        """
        Validate the password fields to check if they are same.
        """
        if not self.confirm_password or not self.new_password:
            raise ValueError('Password cannot be empty')
        return self


# Define the LoginRequest model
class LoginRequest(UserNameModel):
    """
    Model for login request.
    """
    code: str = Field(..., min_length=4, max_length=64,
            description="Password or OTP",
            examples=["123456"]
        )


# Define the ForgotPasswordRequest model
class ForgotPasswordRequest(UserNameModel):
    """
    Model for forgot password request.
    """
    pass


# Define the ChangePasswordRequest model
class ChangePasswordRequest(PasswordModel):
    """
    Model for change password request.
    """
    old_password: str = Field(..., min_length=8, max_length=64,
            description="Old Password"
        )


# Define the RegisterRequest model
class RegisterRequest(BaseModel):
    """
    Model for register request.
    """
    name: str = Field(..., min_length=2, max_length=64,
            description="Name of the user",
            examples=["John Doe"]
        )
    email: EmailStr = Field(..., description="Email of the user",
            examples=["name@company.com"]
        )
    phone_number: PhoneNumber | None = Field(default=None,
            description="Phone Number in E164 format", 
            examples=["+14155552671"]
        )

    @model_validator(mode='after')
    def check_email_domain(self) -> Self:
        """
        Validate the email domain to check if it is allowed.
        """
        if self.email:
            email_domain = str(self.email).split('@')[1]
            if email_domain in config.RESTRICTED_DOMAINS:
                raise ValueError('Invalid email domain')
        return self


# Define the ResetPasswordRequest model
class ResetPasswordRequest(PasswordModel):
    """
    Model for reset password request.
    """
    token: str = Field(..., min_length=8, max_length=64,
            description="Reset Password Token"
        )
