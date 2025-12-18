from __future__ import annotations
import random
from typing import Type, List

from src.entities.trap import SpikeTrap, LavaPool

TRAP_REGISTRY: List[Type[SpikeTrap | LavaPool]] = [SpikeTrap, LavaPool]

def get_random_trap() -> Type[SpikeTrap | LavaPool]:
    return random.choice(TRAP_REGISTRY)

