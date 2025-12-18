from __future__ import annotations
import random
from typing import Type, List

from src.entities.items import Item, Magnet, Bomb, Scissors, RottenApple

# Simple registry for items; can be extended with tags/weights
ITEM_REGISTRY: List[Type[Item]] = [Magnet, Bomb, Scissors, RottenApple]

def get_random_item() -> Type[Item]:
    return random.choice(ITEM_REGISTRY)

