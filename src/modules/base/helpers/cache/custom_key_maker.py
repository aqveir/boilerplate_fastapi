import inspect
from typing import Callable

from base.helpers.cache.base import BaseKeyMaker


class CustomKeyMaker(BaseKeyMaker):
    async def make(self, *, function: Callable, prefix: str) -> str:
        path = f"{prefix}::{inspect.getmodule(function).__name__}.{function.__name__}"  # type: ignore
        args = ""

        for arg in inspect.signature(function).parameters.values():
            args += arg.name

        if args:
            return f"{path}.{args}"

        return path
