from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Type, Optional, Any
import uuid

if TYPE_CHECKING:
    from .component import Component
    from .world import World

class Entity:
    def __init__(self, world: "World", entity_id: Optional[str] = None):
        self.world = world
        self.id = entity_id or str(uuid.uuid4())
        self._components: Dict[Type[Component], Component] = {}
        self.active = True
        self.tags: set[str] = set()

    def add_component(self, component: "Component") -> "Entity":
        component_type = type(component)
        self._components[component_type] = component
        component.entity = self
        self.world._register_component(self, component_type)
        return self

    def get_component(self, component_type: Type["Component"]) -> Optional["Component"]:
        return self._components.get(component_type)

    def has_component(self, component_type: Type["Component"]) -> bool:
        return component_type in self._components

    def remove_component(self, component_type: Type["Component"]) -> "Entity":
        if component_type in self._components:
            del self._components[component_type]
            self.world._unregister_component(self, component_type)
        return self

    def get_all_components(self) -> Dict[Type["Component"], "Component"]:
        return self._components.copy()

    def add_tag(self, tag: str) -> "Entity":
        self.tags.add(tag)
        return self

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    def remove_tag(self, tag: str) -> "Entity":
        self.tags.discard(tag)
        return self

    def destroy(self):
        self.active = False
        self.world.destroy_entity(self)

    def __repr__(self) -> str:
        return f"Entity(id={self.id[:8]}, components={list(self._components.keys())})"
