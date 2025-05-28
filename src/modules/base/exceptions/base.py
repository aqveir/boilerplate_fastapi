""" Import the required modules """
import logging
from http import HTTPStatus
from botocore.exceptions import ClientError

# Set Error logger
logger = logging.getLogger("error")

# Generic Exception : 400
class GenericBaseException(Exception):
    """ Generic Base Exception

    This is the base exception class for all the exceptions in the project.
    It inherits from the built-in Exception class and provides a
    standardized way to handle exceptions in the project.
    It includes the following attributes:
    - status_code: The HTTP status code for the exception.
    - error_code: The error code for the exception.
    - error_msg_code: The error message code for the exception.
    - message: The error message for the exception.
    """
    status_code: int = HTTPStatus.BAD_REQUEST.value
    error_code: str = HTTPStatus.BAD_REQUEST.phrase
    error_msg_code: str = 'error_code_generic'
    message: str = HTTPStatus.BAD_REQUEST.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(self.message)

    def __str__(self):
        return (
            f"<GenericBaseException {self.__class__} - "
            + f"status_code={self.status_code} - context={self.__context__}>"
        )

# Bad Request Exception : 400
class BadRequestException(GenericBaseException):
    """ Bad Request Exception : 400
    This exception is used when a request is made with invalid data or
    when the request cannot be processed due to client error.
    """
    error_msg_code: str = 'error_code_bad_request'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Duplicate Value Exception : 400
class DuplicateValueException(BadRequestException):
    """ Duplicate Value Exception : 400

    This exception is used when a request is made with duplicate values
    or when a request cannot be processed due to duplicate values.
    """
    error_msg_code = 'error_code_duplicate_value'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Entity Not Found Exception : 400
class EntityNotFoundException(BadRequestException):
    """ Entity Not Found Exception : 400 

    This exception is used when an entity is not found in the database 
    or when a request is made with an invalid entity ID.
    """
    error_msg_code = 'error_code_entity_not_found'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Entity Not Found Exception : 400
class EntityNotSavedException(BadRequestException):
    """ Entity Not Saved Exception : 400 

    This exception is used when an entity is not saved in the database 
    or when a request is made with an invalid entity ID.
    """
    error_msg_code = 'error_code_entity_not_saved'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Authentication Exception : 401
class AuthenticationException(GenericBaseException):
    """ Authentication Exception : 401

    This exception is used when a request is made without authentication
    or when the authentication credentials are invalid.
    """
    status_code: int = HTTPStatus.UNAUTHORIZED.value
    error_code: str = HTTPStatus.UNAUTHORIZED.phrase
    error_msg_code: str = 'error_code_authentication'
    message: str = HTTPStatus.UNAUTHORIZED.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=self.error_msg_code)

# Invalid Token Exception : 401
class InvalidTokenException(AuthenticationException):
    """ Invalid Token Exception : 401

    This exception is used when a request is made with an invalid token
    or when the token is expired.
    """
    error_msg_code: str = 'error_code_invalid_token'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Forbidden Exception : 403
class ForbiddenException(GenericBaseException):
    """ Forbidden Exception : 403

    This exception is used when a request is made without permission
    or when the request is not allowed.
    """
    status_code: int = HTTPStatus.FORBIDDEN.value
    error_code: str = HTTPStatus.FORBIDDEN.phrase
    error_msg_code: str = 'error_code_forbidden'
    message: str = HTTPStatus.FORBIDDEN.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Unauthorized Exception : 403
class UnauthorizedException(ForbiddenException):
    """ Unauthorized Exception : 403

    This exception is used when a request is made without authentication
    or when the request is not allowed.
    """
    error_msg_code = 'error_code_unauthorized'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Not Found Exception : 404
class NotFoundException(GenericBaseException):
    """ Not Found Exception : 404
    This exception is used when a request is made with an invalid URL
    or when the requested resource is not found.
    """
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    error_msg_code = 'error_code_not_found'
    message = HTTPStatus.NOT_FOUND.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Unprocessable Entity Exception : 422
class UnprocessableEntity(GenericBaseException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_msg_code = 'error_code_unprocessable_entity'
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=message, error_msg_code=error_msg_code)

# Model Validation Exception : 422
class ModelValidationException(GenericBaseException):
    code = HTTPStatus.UNPROCESSABLE_CONTENT
    error_code = HTTPStatus.UNPROCESSABLE_CONTENT
    error_msg_code = 'error_code_model_validation'
    message = HTTPStatus.UNPROCESSABLE_CONTENT.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=self.message, error_msg_code=self.error_msg_code)

# Internal Server Error Exception : 500
class InternalServerErrorException(GenericBaseException):
    """ Internal Server Error Exception : 500

    This exception is used when a request cannot be processed
    due to an internal server error.
    """
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_msg_code = 'error_code_internal_server_error'
    message = HTTPStatus.INTERNAL_SERVER_ERROR.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=self.message, error_msg_code=self.error_msg_code)

# AWS Exception : 400
class AWSValueException(BadRequestException):
    """ AWS Exception : 400

    This exception is used when a request is made with invalid AWS values
    or when a request cannot be processed due to invalid AWS values.
    """
    error_msg_code = 'error_code_aws'

    def __init__(self, exception: ClientError, error_msg_code: str|None=None):
        if exception:
            self.message = exception.response["Error"]["Message"]
        if error_msg_code:
            self.error_msg_code = error_msg_code

        super().__init__(message=self.message, error_msg_code=error_msg_code)
