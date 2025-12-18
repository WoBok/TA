from __future__ import annotations
from typing import Type

from src.entities.items import Item, Magnet, Bomb, Scissors, RottenApple, ScoreBoost
from src.registries.registry import Registry

# Simple registry for items; can be extended with tags/weights
ITEM_REGISTRY: Registry[Type[Item]] = Registry()
ITEM_REGISTRY.register(Magnet)
ITEM_REGISTRY.register(Bomb)
ITEM_REGISTRY.register(Scissors)
ITEM_REGISTRY.register(RottenApple)
ITEM_REGISTRY.register(ScoreBoost, weight=0)

def get_random_item() -> Type[Item]:
    return ITEM_REGISTRY.choose_random()
