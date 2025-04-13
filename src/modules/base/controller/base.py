from typing import Any, Generic, Type, TypeVar

from ..db import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseController(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model