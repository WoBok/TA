import pygame
import random
from typing import List

from src.core.scene import Scene
from src.systems.fixed_step_system import FixedStepSystem
from src.systems.game_tuning import GameTuning
from src.systems.hud_renderer import HudRenderer
from src.systems.spawn_system import SpawnSystem
from src.managers.input_manager import InputManager
from src.managers.leaderboard import load_leaderboard
from src.entities.particle import ParticleSystem
from src.entities.snake import Snake
from src.entities.food import Food, EnergyFood
from src.entities.obstacle import Obstacles
from src.entities.items import Item
from src.entities.portal import PortalPair
from src.entities.trap import SpikeTrap, LavaPool
from src.entities.enemy import GhostHunter
from src.entities.enemy_types import AIEnemy
from src.entities.boss import Boss
from src.managers.effects import EffectsManager
from src.scenes.scene_keys import (
    SCENE_GAME_OVER,
    SCENE_MENU,
    SCENE_OVERLAY_LEADERBOARD,
    SCENE_OVERLAY_PAUSE,
    SCENE_OVERLAY_SETTINGS,
    SCENE_OVERLAY_HELP,
)

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GAME_AREA_Y, BG_COLOR, GRID_COLOR, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    STEP_INTERVAL_MS, GHOST_DURATION, BOTTOM_BAR_HEIGHT,
)

class GameScene(Scene):
    """Main gameplay scene with all features including combo system and boss fights."""

    def __init__(self, app: "GameApp"):
        super().__init__(app)
        self.ui = self.app.services["ui"]
        self.settings = self.app.services["settings"]
        self.tuning: GameTuning = GameTuning.from_settings(self.settings)

        self.spawner = SpawnSystem()
        self.fixed_stepper = FixedStepSystem()
        self.hud_renderer = HudRenderer()

        self.input_manager = InputManager()
        self.particles = ParticleSystem()
        self.effects = EffectsManager(self.particles, self.input_manager)
        self.events = self.app.services["events"]
        self.leaderboard = load_leaderboard()
        self.grid_surface = None
        self._build_grid_surface()
        self.reset()

    def reset(self):
        self.snake = Snake([(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)])
        self.obstacles = Obstacles()
        self.food: Food | None = None
        self.energy_food: EnergyFood | None = None
        self.items: List[Item] = []
        self.portals: PortalPair | None = None
        self.traps: List[SpikeTrap | LavaPool] = []
        self.ai_snakes: List[AIEnemy] = []
        self.ghost_hunters: List[GhostHunter] = [GhostHunter(pos=(0,0)) for _ in range(3)]
        self.boss: Boss | None = None

        self.score = 0
        self.energy = 1
        self.normal_food_eaten_total = 0
        self.food_for_boss_counter = 0
        self.combo_multiplier = 1
        self.last_food_eat_time = 0
        self.combo_window = int(self.tuning.combo_window_ms) # 2 seconds

        self.ghost_mode = False
        self.ghost_end_time = 0
        self.last_item_spawn_time = pygame.time.get_ticks()
        self.last_ai_spawn_time = pygame.time.get_ticks()
        self.item_spawn_interval = int(self.tuning.item_spawn_interval_ms)
        self.ai_spawn_interval = random.randint(
            int(self.tuning.ai_spawn_interval_min_ms),
            int(self.tuning.ai_spawn_interval_max_ms),
        )
        self.step_interval_ms = STEP_INTERVAL_MS
        self.move_accum = 0.0

        self.spawn_environment()
        self.spawn_food()

    def _maybe_print_exception(self) -> None:
        try:
            if getattr(self.settings, "debug_exceptions", False):
                import traceback

                traceback.print_exc()
        except Exception:
            pass

    def random_empty_cell(self, size=(1,1)) -> tuple[int, int] | None:
        occupied = set(self.snake.body) | self.obstacles.cells
        if self.food: occupied.add(self.food.pos)
        if self.energy_food: occupied.add(self.energy_food.pos)
        for item in self.items: occupied.add(item.pos)
        if self.portals:
            occupied.add(self.portals.orange)
            occupied.add(self.portals.blue)
        for trap in self.traps:
            occupied.add(trap.pos)
        for ai in self.ai_snakes:
            occupied.update(ai.body)
        
        possible_positions = []
        for y in range(GRID_HEIGHT - size[1] + 1):
            for x in range(GRID_WIDTH - size[0] + 1):
                is_free = True
                for r in range(size[1]):
                    for c in range(size[0]):
                        if (x + c, y + r) in occupied:
                            is_free = False
                            break
                    if not is_free: break
                if is_free:
                    possible_positions.append((x,y))
        
        return random.choice(possible_positions) if possible_positions else None

    def handle_food_eat(self, now: int):
        if now - self.last_food_eat_time < self.combo_window:
            self.combo_multiplier = min(8, self.combo_multiplier * 2)
        else:
            self.combo_multiplier = 1
        self.last_food_eat_time = now

        self.score += 1 * self.combo_multiplier
        self.normal_food_eaten_total += 1
        self.food_for_boss_counter += 1

        if self.food_for_boss_counter >= int(self.tuning.boss_food_threshold):
            self.food_for_boss_counter = 0
            self.spawn_boss()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN:
                direction = None
                if e.key in (pygame.K_UP, pygame.K_w): direction = (0, -1)
                elif e.key in (pygame.K_DOWN, pygame.K_s): direction = (0, 1)
                elif e.key in (pygame.K_LEFT, pygame.K_a): direction = (-1, 0)
                elif e.key in (pygame.K_RIGHT, pygame.K_d): direction = (1, 0)
                
                if direction:
                    if self.input_manager.inverted: direction = (-direction[0], -direction[1])
                    self.snake.set_direction(direction)
                
                elif e.key == pygame.K_SPACE:
                    self.toggle_ghost_mode()
                elif e.key == pygame.K_TAB:
                    self.app.push_scene_key(SCENE_OVERLAY_LEADERBOARD)
                    # Let overlay show "(游戏已暂停)" subtitle
                    overlay = self.app.current_scene
                    try:
                        overlay.with_subtitle("(游戏已暂停)")  # type: ignore[attr-defined]
                    except Exception:
                        self._maybe_print_exception()
                elif e.key == pygame.K_p:
                    self.app.push_scene_key(SCENE_OVERLAY_PAUSE)
                elif e.key == pygame.K_o:
                    self.app.push_scene_key(SCENE_OVERLAY_SETTINGS)
                elif e.key == pygame.K_h:
                    self.app.push_scene_key(SCENE_OVERLAY_HELP)
                elif e.key == pygame.K_ESCAPE:
                    self.app.push_scene_key(SCENE_MENU)

    def spawn_environment(self):
        self.spawner.spawn_environment(self)

    def spawn_food(self):
        self.spawner.spawn_food(self)

    def spawn_obstacle(self):
        self.spawner.spawn_obstacle(self)

    def spawn_item(self):
        self.spawner.spawn_item(self)

    def spawn_ai_snake(self):
        self.spawner.spawn_ai_snake(self)

    def spawn_boss(self):
        self.spawner.spawn_boss(self)

    def shrink_snake(self, amount: int):
        if len(self.snake.body) <= 3: return
        shrink_amount = min(amount, len(self.snake.body) - 3)
        removed_parts = self.snake.body[-shrink_amount:]
        self.snake.body = self.snake.body[:-shrink_amount]
        self.effects.trigger_shrink_effect(removed_parts)

    def toggle_ghost_mode(self):
        now = pygame.time.get_ticks()
        if self.ghost_mode:
            self.ghost_mode = False
        elif self.energy > 0:
            self.energy -= 1
            self.ghost_mode = True
            self.ghost_end_time = now + GHOST_DURATION

    def trigger_game_over(self, reason: str):
        from src.scenes.game_over_scene import GameOverScene
        self.app.push_scene_key(SCENE_GAME_OVER)
        game_over_scene = self.app.current_scene
        if isinstance(game_over_scene, GameOverScene):
            game_over_scene.set_stats(self.score, reason, self.leaderboard)

    def update_fixed(self, dt: float) -> None:
        self.fixed_stepper.update_fixed(self, dt)

    def update(self, dt: float) -> None:
        now = pygame.time.get_ticks()
        # Variable-step systems
        self.particles.update()
        self.effects.update(self.snake.head(), [self.food, self.energy_food])
        for trap in self.traps:
            if isinstance(trap, LavaPool):
                trap.update()
        for hunter in self.ghost_hunters:
            hunter.update(self.snake.head())
        if self.boss:
            self.boss.update(self.snake.head())

        # Timed spawns
        if now - self.last_item_spawn_time > self.item_spawn_interval and len(self.items) < int(self.tuning.max_items):
            self.spawn_item()
        if now - self.last_ai_spawn_time > self.ai_spawn_interval and len(self.ai_snakes) < int(self.tuning.max_ai_snakes):
            self.spawn_ai_snake()

        # Timers/flags
        if self.ghost_mode and now >= self.ghost_end_time:
            self.ghost_mode = False
        if now - self.last_food_eat_time > self.combo_window:
            self.combo_multiplier = 1

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG_COLOR)
        if self.grid_surface:
            surface.blit(self.grid_surface, (0, 0))
        if self.portals: self.portals.draw(surface)
        for trap in self.traps: trap.draw(surface)
        self.obstacles.draw(surface)
        if self.food: self.food.draw(surface)
        if self.energy_food: self.energy_food.draw(surface)
        for item in self.items: item.draw(surface, CELL_SIZE, GAME_AREA_Y)
        for ai in self.ai_snakes: ai.draw(surface)
        if self.boss: self.boss.draw(surface)
        
        ghost_alpha = None
        if self.ghost_mode:
            time_left = max(0, self.ghost_end_time - pygame.time.get_ticks())
            interval = 50 if time_left < 2000 else 100 if time_left < 3000 else 150
            ghost_alpha = 120 if (pygame.time.get_ticks() // interval) % 2 == 0 else 200

        self.snake.draw(surface, ghost_alpha, rainbow_effect=self.effects.is_rainbow_trail_active)
        for hunter in self.ghost_hunters: hunter.draw(surface)
        
        self.particles.draw(surface)
        self.draw_hud(surface)
        self.draw_bottom_bar(surface)

    def _build_grid_surface(self):
        game_area_end_y = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # 边框
        border_color = (100, 50, 150)
        pygame.draw.line(surf, border_color, (0, GAME_AREA_Y), (SCREEN_WIDTH, GAME_AREA_Y), 2)
        pygame.draw.line(surf, border_color, (0, GAME_AREA_Y), (0, game_area_end_y), 2)
        pygame.draw.line(surf, border_color, (0, game_area_end_y - 1), (SCREEN_WIDTH, game_area_end_y - 1), 2)
        pygame.draw.line(surf, border_color, (SCREEN_WIDTH - 1, GAME_AREA_Y), (SCREEN_WIDTH - 1, game_area_end_y), 2)
        # 小格
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(surf, GRID_COLOR, (x, GAME_AREA_Y), (x, game_area_end_y), 1)
        for y in range(GAME_AREA_Y, game_area_end_y, CELL_SIZE):
            pygame.draw.line(surf, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        # 5x5 大格
        bright_grid = (80, 40, 120)
        for x in range(0, SCREEN_WIDTH, CELL_SIZE * 5):
            pygame.draw.line(surf, bright_grid, (x, GAME_AREA_Y), (x, game_area_end_y), 2)
        for y in range(GAME_AREA_Y, game_area_end_y, CELL_SIZE * 5):
            pygame.draw.line(surf, bright_grid, (0, y), (SCREEN_WIDTH, y), 2)
        self.grid_surface = surf

    def draw_hud(self, surface: pygame.Surface):
        self.hud_renderer.draw_hud(self, surface)

    def draw_bottom_bar(self, surface: pygame.Surface):
        self.hud_renderer.draw_bottom_bar(self, surface)
