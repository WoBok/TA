from __future__ import annotations

import pygame

from config import (
    CELL_SIZE,
    FOOD_COLOR,
    ENERGY_FOOD_COLOR,
    FOOD_PER_OBSTACLE,
    GAME_AREA_Y,
    EVT_FOOD_EATEN,
    EVT_ENERGY_EATEN,
)

from src.entities.food import EnergyFood
from src.rules.step_rules import (
    RulePipeline,
    build_default_pre_enemy_pipeline,
    build_default_post_enemy_pipeline,
)


class FixedStepSystem:
    def __init__(
        self,
        pre_enemy_pipeline: RulePipeline | None = None,
        post_enemy_pipeline: RulePipeline | None = None,
    ) -> None:
        self.pre_enemy_pipeline = pre_enemy_pipeline or build_default_pre_enemy_pipeline()
        self.post_enemy_pipeline = post_enemy_pipeline or build_default_post_enemy_pipeline()

    def update_fixed(self, game, dt: float) -> None:
        game.move_accum += dt
        step_sec = game.step_interval_ms / 1000.0
        steps = int(game.move_accum // step_sec)
        if steps <= 0:
            return
        game.move_accum -= steps * step_sec

        for _ in range(steps):
            ate_food = False
            game.snake.step(ate_food)
            player_head = game.snake.head()
            player_head, result = self.pre_enemy_pipeline.apply(game, player_head)
            if result:
                return game.trigger_game_over(result.reason)

            foods_pos = [f.pos for f in [game.food, game.energy_food] if f]
            for ai in game.ai_snakes[:]:
                ai.update_ai(foods_pos)
                ai.step()
                ai_head = ai.head()
                if game.food and ai_head == game.food.pos:
                    game.food = None
                    ai.step(grow=True)
                if game.energy_food and ai_head == game.energy_food.pos:
                    game.energy_food = None
                    ai.step(grow=True)
                if ai_head in game.snake.body:
                    game.ai_snakes.remove(ai)
                    for _ in range(5):
                        pos = game.random_empty_cell()
                        if pos:
                            game.energy_food = EnergyFood(pos)

            player_head, result = self.post_enemy_pipeline.apply(game, player_head)
            if result:
                return game.trigger_game_over(result.reason)

            now = pygame.time.get_ticks()

            if game.food and player_head == game.food.pos:
                ate_food = True
                game.handle_food_eat(now)
                game.particles.emit(
                    player_head[0] * CELL_SIZE + CELL_SIZE // 2,
                    GAME_AREA_Y + player_head[1] * CELL_SIZE + CELL_SIZE // 2,
                    FOOD_COLOR,
                    25,
                )
                game.snake.trigger_glow(FOOD_COLOR, now)
                game.events.publish(
                    EVT_FOOD_EATEN,
                    {"pos": player_head, "score": game.score, "combo": game.combo_multiplier},
                )
                game.food = None
                if game.normal_food_eaten_total % FOOD_PER_OBSTACLE == 0:
                    game.spawn_obstacle()

            if game.energy_food and player_head == game.energy_food.pos:
                ate_food = True
                game.energy += 1
                game.particles.emit(
                    player_head[0] * CELL_SIZE + CELL_SIZE // 2,
                    GAME_AREA_Y + player_head[1] * CELL_SIZE + CELL_SIZE // 2,
                    ENERGY_FOOD_COLOR,
                    30,
                )
                game.snake.trigger_glow(ENERGY_FOOD_COLOR, now)
                game.events.publish(
                    EVT_ENERGY_EATEN,
                    {"pos": player_head, "energy": game.energy},
                )
                game.energy_food = None

            for item in game.items[:]:
                if player_head == item.pos:
                    item.apply(game)
                    game.items.remove(item)

            if ate_food and game.snake.body:
                game.snake.body.append(game.snake.body[-1])

            if game.food is None:
                game.spawn_food()
