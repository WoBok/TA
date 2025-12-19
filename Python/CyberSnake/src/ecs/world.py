from __future__ import annotations
from typing import Dict, List, Set, Type, Optional, Any
from collections import defaultdict

from .entity import Entity
from .component import Component
from .system import System

class World:
    def __init__(self):
        self._entities: Dict[str, Entity] = {}
        self._systems: List[System] = []
        self._component_index: Dict[Type[Component], Set[Entity]] = defaultdict(set)
        self._entities_to_destroy: List[Entity] = []

    def create_entity(self, entity_id: Optional[str] = None) -> Entity:
        entity = Entity(self, entity_id)
        self._entities[entity.id] = entity
        return entity

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        return self._entities.get(entity_id)

    def destroy_entity(self, entity: Entity):
        if entity not in self._entities_to_destroy:
            self._entities_to_destroy.append(entity)

    def _process_entity_destruction(self):
        for entity in self._entities_to_destroy:
            for component_type in list(entity._components.keys()):
                entity.remove_component(component_type)
            if entity.id in self._entities:
                del self._entities[entity.id]
        self._entities_to_destroy.clear()

    def get_all_entities(self) -> List[Entity]:
        return [e for e in self._entities.values() if e.active]

    def get_entities_with_components(self, *component_types: Type[Component]) -> List[Entity]:
        if not component_types:
            return self.get_all_entities()
        
        result_sets = [self._component_index.get(ct, set()) for ct in component_types]
        if not result_sets:
            return []
        
        intersection = set.intersection(*result_sets)
        return [e for e in intersection if e.active]

    def get_entities_with_tag(self, tag: str) -> List[Entity]:
        return [e for e in self._entities.values() if e.active and e.has_tag(tag)]

    def add_system(self, system: System) -> System:
        self._systems.append(system)
        self._systems.sort(key=lambda s: s.priority)
        return system

    def remove_system(self, system: System):
        if system in self._systems:
            self._systems.remove(system)

    def update(self, dt: float):
        for system in self._systems:
            if system.enabled:
                system.update(dt)
        self._process_entity_destruction()

    def _register_component(self, entity: Entity, component_type: Type[Component]):
        self._component_index[component_type].add(entity)

    def _unregister_component(self, entity: Entity, component_type: Type[Component]):
        self._component_index[component_type].discard(entity)

    def clear(self):
        for entity in list(self._entities.values()):
            entity.destroy()
        self._process_entity_destruction()
        self._systems.clear()
        self._component_index.clear()
