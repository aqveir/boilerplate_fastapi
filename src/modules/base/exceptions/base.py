# class SkyPulseApiError(Exception):
#     """base exception class"""

#     def __init__(self, message: str = "Service is unavailable", name: str = "SkyPulse"):
#         self.message = message
#         self.name = name
#         super().__init__(self.message, self.name)


# class ServiceError(SkyPulseApiError):
#     """failures in external services or APIs, like a database or a third-party service"""

#     pass


# class EntityDoesNotExistError(SkyPulseApiError):
#     """database returns nothing"""

#     pass


# class EntityAlreadyExistsError(SkyPulseApiError):
#     """conflict detected, like trying to create a resource that already exists"""

#     pass


# class InvalidOperationError(SkyPulseApiError):
#     """invalid operations like trying to delete a non-existing entity, etc."""

#     pass


# class AuthenticationFailed(SkyPulseApiError):
#     """invalid authentication credentials"""

#     pass


# class InvalidTokenError(SkyPulseApiError):
#     """invalid token"""

#     pass

from http import HTTPStatus
from fastapi import HTTPException, status


class GenericBaseException(Exception):
    status_code: int = HTTPStatus.BAD_REQUEST.value
    error_code: str = HTTPStatus.BAD_REQUEST.phrase
    error_msg_code: str = 'error_code_generic'
    message: str = HTTPStatus.BAD_REQUEST.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code
        super().__init__(message=self.message)

    def __str__(self):
        return (
            f"<GenericBaseException {self.__class__} - "
            + f"status_code={self.status_code} - context={self.__context__}>"
        )

# Bad Request Exception : 400
class BadRequestException(GenericBaseException):
    error_msg_code: str = 'error_code_bad_request'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

# Duplicate Value Exception : 400
class DuplicateValueException(BadRequestException):
    error_msg_code = 'error_code_duplicate_value'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code


""" Entity Not Found Exception : 400 

This exception is used when an entity is not found in the database 
or when a request is made with an invalid entity ID.
"""
class EntityNotFoundException(BadRequestException):
    error_msg_code = 'error_code_entity_not_found'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

# Authentication Exception : 401
class AuthenticationException(GenericBaseException):
    status_code: int = HTTPStatus.UNAUTHORIZED.value
    error_code: str = HTTPStatus.UNAUTHORIZED.phrase
    error_msg_code: str = 'error_code_authentication'
    message: str = HTTPStatus.UNAUTHORIZED.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

# Invalid Token Exception : 401
class InvalidTokenException(AuthenticationException):
    error_msg_code: str = 'error_code_invalid_token'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code    

# Forbidden Exception : 403
class ForbiddenException(GenericBaseException):
    status_code: int = HTTPStatus.FORBIDDEN.value
    error_code: str = HTTPStatus.FORBIDDEN.phrase
    error_msg_code: str = 'error_code_forbidden'
    message: str = HTTPStatus.FORBIDDEN.description

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

# Unauthorized Exception : 403
class UnauthorizedException(ForbiddenException):
    error_msg_code = 'error_code_unauthorized'

    def __init__(self, message: str|None=None, error_msg_code: str|None=None):
        if message:
            self.message = message
        if error_msg_code:
            self.error_msg_code = error_msg_code

# Not Found Exception : 404
class NotFoundException(GenericBaseException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    error_msg_code = 'error_code_not_found'
    message = HTTPStatus.NOT_FOUND.description

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.error_msg_code = code

        super().__init__(message=message, code=code)

# Unprocessable Entity Exception : 422
class UnprocessableEntity(GenericBaseException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_msg_code = 'error_code_unprocessable_entity'
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.error_msg_code = code

        super().__init__(message=message, code=code)

# Model Validation Exception : 422
class ModelValidationException(GenericBaseException):
    code = HTTPStatus.UNPROCESSABLE_CONTENT
    error_code = HTTPStatus.UNPROCESSABLE_CONTENT
    error_msg_code = 'error_code_model_validation'
    message = HTTPStatus.UNPROCESSABLE_CONTENT.description

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.error_msg_code = code

        super().__init__(message=message, code=code)

# Internal Server Error Exception : 500
class InternalServerErrorException(GenericBaseException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_msg_code = 'error_code_internal_server_error'
    message = HTTPStatus.INTERNAL_SERVER_ERROR.description

    def __init__(self, message=None, code=None):
        if message:
            self.message = message
        if code:
            self.error_msg_code = code

        super().__init__(message=message, code=code)






