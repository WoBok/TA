from __future__ import annotations
from typing import Type

from src.entities.trap import SpikeTrap, LavaPool
from src.registries.registry import Registry

TRAP_REGISTRY: Registry[Type[SpikeTrap | LavaPool]] = Registry()
TRAP_REGISTRY.register(SpikeTrap)
TRAP_REGISTRY.register(LavaPool)

def get_random_trap() -> Type[SpikeTrap | LavaPool]:
    return TRAP_REGISTRY.choose_random()
