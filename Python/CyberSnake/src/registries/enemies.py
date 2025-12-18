from __future__ import annotations

from typing import Type

from src.entities.enemy import AISnake, WanderingAISnake
from src.entities.enemy_types import AIEnemy
from src.registries.registry import Registry

ENEMY_REGISTRY: Registry[Type[AIEnemy]] = Registry()
ENEMY_REGISTRY.register(AISnake)
ENEMY_REGISTRY.register(WanderingAISnake, weight=0)


def get_random_enemy() -> Type[AIEnemy]:
    return ENEMY_REGISTRY.choose_random()
