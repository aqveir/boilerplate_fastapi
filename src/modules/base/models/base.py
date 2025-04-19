from typing import Generic, List, Optional, TypeVar, Union

from uuid import UUID, uuid1
from datetime import datetime, date
from fastapi import status
from pydantic import (BaseModel, Field, SerializeAsAny, computed_field, field_serializer)

T = TypeVar('T')

class ApplicationBaseModel(BaseModel):
    """
    Base model for the application.
    """
    id: int = Field(..., description="UID", exclude=True)


class AppBaseModelWithHash(ApplicationBaseModel):
    """
    Base model for the application with hash.
    """
    hash: UUID = Field(default_factory=lambda: uuid1(), description="Hash")

    @field_serializer('hash', when_used='json')
    def serialize_hash(self, value: UUID) -> str:
        return str(value)


class AppBaseModelWithAuditLog(ApplicationBaseModel):
    """
    Base model for the application with hash and audit log.
    """

    created_by: int = Field(default=0, description="Created By", exclude=True)
    created_at: datetime = Field(default_factory=datetime.now, description="Created At", exclude=True)
    updated_by: int = Field(default=None, description="Updated By", exclude=True)
    updated_at: datetime = Field(default=None, description="Updated At", exclude=True)
    deleted_by: int = Field(default=None, description="Deleted By", exclude=True)
    deleted_at: datetime = Field(default=None, description="Deleted At", exclude=True)

    is_active: int = Field(default=1, description="Is Active", exclude=True)

    @computed_field
    @property
    def last_modified_at(self) -> datetime:
        return_value: datetime = None

        if self.deleted_at:
            return_value = self.deleted_at
        elif self.updated_at and self.updated_at > self.created_at:
            return_value = self.updated_at
        else:
            return_value = self.created_at

        return return_value
    

class AppBaseModelWithHashAndAuditLog(AppBaseModelWithAuditLog):
    """
    Base model for the application with hash.
    """
    hash: UUID = Field(default_factory=lambda: uuid1(), description="Hash")

    @field_serializer('hash', when_used='json')
    def serialize_hash(self, value: UUID) -> str:
        return str(value)
    
    
class GenericResponse(BaseModel, Generic[T]):
    status_code: int
    message: str
    success: bool = True
    data: Optional[SerializeAsAny[T]] = None
    errors: Optional[SerializeAsAny[dict]] = None
    metadata: Optional[SerializeAsAny[dict]] = None


class GenericSuccessResponse(GenericResponse, Generic[T]):
    status_code: int = status.HTTP_200_OK
    message: str = "success"
    success: bool = True
    data: Optional[SerializeAsAny[T]] = None
    metadata: Optional[SerializeAsAny[dict]] = None
