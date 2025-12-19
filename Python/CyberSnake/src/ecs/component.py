from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .entity import Entity

class Component:
    def __init__(self):
        self.entity: "Entity" | None = None

    def on_add(self):
        pass

    def on_remove(self):
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
