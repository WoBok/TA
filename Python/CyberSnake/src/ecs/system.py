from __future__ import annotations
from typing import TYPE_CHECKING, List, Type
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .world import World
    from .component import Component

class System(ABC):
    def __init__(self, world: "World"):
        self.world = world
        self.enabled = True
        self.priority = 0

    @abstractmethod
    def update(self, dt: float):
        pass

    def get_entities_with_components(self, *component_types: Type["Component"]) -> List:
        return self.world.get_entities_with_components(*component_types)

    def on_enable(self):
        pass

    def on_disable(self):
        pass
