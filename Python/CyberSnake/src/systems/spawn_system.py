from __future__ import annotations

import random

import pygame

from src.entities.boss import Boss
from src.entities.food import Food, EnergyFood
from src.entities.portal import PortalPair
from src.registries.enemies import get_random_enemy
from src.registries.items import get_random_item
from src.registries.traps import get_random_trap


class SpawnSystem:
    def spawn_environment(self, game) -> None:
        p1, p2 = game.random_empty_cell(), game.random_empty_cell()
        if p1 and p2:
            game.portals = PortalPair(orange=p1, blue=p2)
        for _ in range(random.randint(game.tuning.traps_min, game.tuning.traps_max)):
            pos = game.random_empty_cell()
            if pos:
                trap_cls = get_random_trap()
                game.traps.append(trap_cls(pos=pos))

    def spawn_food(self, game) -> None:
        pos = game.random_empty_cell()
        if pos:
            game.food = Food(pos)
        if game.energy_food is None and random.random() < float(game.tuning.energy_food_spawn_chance):
            pos = game.random_empty_cell()
            if pos:
                game.energy_food = EnergyFood(pos)

    def spawn_obstacle(self, game) -> None:
        pos = game.random_empty_cell()
        if pos:
            game.obstacles.add(pos)

    def spawn_item(self, game) -> None:
        pos = game.random_empty_cell()
        if pos:
            item_cls = get_random_item()
            game.items.append(item_cls(pos=pos))
            game.last_item_spawn_time = pygame.time.get_ticks()

    def spawn_ai_snake(self, game) -> None:
        start_pos = game.random_empty_cell()
        if start_pos:
            enemy_cls = get_random_enemy()
            game.ai_snakes.append(enemy_cls(body=[start_pos]))
            game.last_ai_spawn_time = pygame.time.get_ticks()

    def spawn_boss(self, game) -> None:
        pos = game.random_empty_cell(size=(3, 3))
        if pos and not game.boss:
            game.boss = Boss(pos=pos)
