import pygame
import random
from typing import List

from src.core.scene import Scene
from src.managers.ui_manager import UIManager
from src.managers.input_manager import InputManager
from src.managers.leaderboard import load_leaderboard
from src.entities.particle import ParticleSystem
from src.entities.snake import Snake
from src.entities.food import Food, EnergyFood
from src.entities.obstacle import Obstacles
from src.entities.items import Item, Magnet, Bomb, Scissors, RottenApple
from src.entities.portal import PortalPair
from src.entities.trap import SpikeTrap, LavaPool
from src.entities.enemy import AISnake, GhostHunter
from src.entities.boss import Boss
from src.managers.effects import EffectsManager

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GAME_AREA_Y, BG_COLOR, GRID_COLOR, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    STEP_INTERVAL_MS, FOOD_PER_OBSTACLE, GHOST_DURATION, TEXT_COLOR, FOOD_COLOR, ENERGY_FOOD_COLOR, BOTTOM_BAR_HEIGHT,
    HUD_HEIGHT,
)

class GameScene(Scene):
    """Main gameplay scene with all features including combo system and boss fights."""

    def __init__(self, app: "GameApp"):
        super().__init__(app)
        self.ui = UIManager()
        self.input_manager = InputManager()
        self.particles = ParticleSystem()
        self.effects = EffectsManager(self.particles, self.input_manager)
        self.leaderboard = load_leaderboard()
        self.reset()

    def reset(self):
        self.snake = Snake([(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)])
        self.obstacles = Obstacles()
        self.food: Food | None = None
        self.energy_food: EnergyFood | None = None
        self.items: List[Item] = []
        self.portals: PortalPair | None = None
        self.traps: List[SpikeTrap | LavaPool] = []
        self.ai_snakes: List[AISnake] = []
        self.ghost_hunters: List[GhostHunter] = [GhostHunter(pos=(0,0)) for _ in range(3)]
        self.boss: Boss | None = None

        self.score = 0
        self.energy = 1
        self.normal_food_eaten_total = 0
        self.food_for_boss_counter = 0
        self.combo_multiplier = 1
        self.last_food_eat_time = 0
        self.combo_window = 2000 # 2 seconds

        self.ghost_mode = False
        self.ghost_end_time = 0
        self.last_move_time = pygame.time.get_ticks()
        self.last_item_spawn_time = pygame.time.get_ticks()
        self.last_ai_spawn_time = pygame.time.get_ticks()
        self.item_spawn_interval = 8000
        self.ai_spawn_interval = random.randint(10000, 15000)
        self.step_interval_ms = STEP_INTERVAL_MS
        self.paused = False

        self.spawn_environment()
        self.spawn_food()

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

    def spawn_boss(self):
        pos = self.random_empty_cell(size=(3,3))
        if pos and not self.boss:
            self.boss = Boss(pos=pos)

    def handle_food_eat(self, now: int):
        if now - self.last_food_eat_time < self.combo_window:
            self.combo_multiplier = min(8, self.combo_multiplier * 2)
        else:
            self.combo_multiplier = 1
        self.last_food_eat_time = now

        self.score += 1 * self.combo_multiplier
        self.normal_food_eaten_total += 1
        self.food_for_boss_counter += 1

        if self.food_for_boss_counter >= 10:
            self.food_for_boss_counter = 0
            self.spawn_boss()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        if self.paused:
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
                    self.paused = False
            return

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
                
                elif e.key == pygame.K_SPACE: self.toggle_ghost_mode()
                elif e.key == pygame.K_TAB: self.paused = True
                elif e.key == pygame.K_ESCAPE:
                    from src.scenes.menu_scene import MenuScene
                    self.app.push_scene(MenuScene)

    def spawn_environment(self):
        p1, p2 = self.random_empty_cell(), self.random_empty_cell()
        if p1 and p2:
            self.portals = PortalPair(orange=p1, blue=p2)
        for _ in range(random.randint(3, 5)):
            pos = self.random_empty_cell()
            if pos:
                self.traps.append(random.choice([SpikeTrap, LavaPool])(pos=pos))

    def spawn_food(self):
        pos = self.random_empty_cell()
        if pos: self.food = Food(pos)
        if self.energy_food is None and random.random() < 0.3:
            pos = self.random_empty_cell()
            if pos: self.energy_food = EnergyFood(pos)

    def spawn_obstacle(self):
        pos = self.random_empty_cell()
        if pos: self.obstacles.add(pos)

    def spawn_item(self):
        pos = self.random_empty_cell()
        if pos: 
            self.items.append(random.choice([Magnet, Bomb, Scissors, RottenApple])(pos=pos))
            self.last_item_spawn_time = pygame.time.get_ticks()

    def spawn_ai_snake(self):
        start_pos = self.random_empty_cell()
        if start_pos:
            self.ai_snakes.append(AISnake(body=[start_pos]))
            self.last_ai_spawn_time = pygame.time.get_ticks()

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
        self.app.push_scene(GameOverScene)
        game_over_scene = self.app.current_scene
        if isinstance(game_over_scene, GameOverScene):
            game_over_scene.set_stats(self.score, reason, self.leaderboard)

    def update(self, dt: float) -> None:
        if self.paused: return
        now = pygame.time.get_ticks()
        
        self.particles.update()
        self.effects.update(self.snake.head(), [self.food, self.energy_food])
        for trap in self.traps: 
            if isinstance(trap, LavaPool): trap.update()
        for hunter in self.ghost_hunters: hunter.update(self.snake.head())
        if self.boss: self.boss.update(self.snake.head())

        if now - self.last_item_spawn_time > self.item_spawn_interval and len(self.items) < 2: self.spawn_item()
        if now - self.last_ai_spawn_time > self.ai_spawn_interval and len(self.ai_snakes) < 1: self.spawn_ai_snake()

        if self.ghost_mode and now >= self.ghost_end_time: self.ghost_mode = False
        if now - self.last_food_eat_time > self.combo_window: self.combo_multiplier = 1

        if now - self.last_move_time < self.step_interval_ms: return
        self.last_move_time = now

        ate_food = False
        self.snake.step(ate_food)
        player_head = self.snake.head()

        if not (0 <= player_head[0] < GRID_WIDTH and 0 <= player_head[1] < GRID_HEIGHT):
            if self.ghost_mode:
                self.snake.body[0] = (player_head[0] % GRID_WIDTH, player_head[1] % GRID_HEIGHT)
                player_head = self.snake.head()
            else: return self.trigger_game_over("撞到边界了！")

        if self.portals:
            teleported_pos = self.portals.teleport(player_head)
            if teleported_pos != player_head:
                self.snake.body[0] = teleported_pos
                player_head = teleported_pos

        for trap in self.traps:
            if trap.is_active() and player_head == trap.pos and not self.ghost_mode:
                return self.trigger_game_over("掉进了陷阱！")

        if player_head in self.obstacles.cells and not self.ghost_mode: return self.trigger_game_over("撞到荆棘了！")
        if player_head in self.snake.body[1:] and not self.ghost_mode: return self.trigger_game_over("撞到自己了！")

        if self.boss:
            for bullet in self.boss.bullets:
                if bullet.get_grid_pos() == player_head and not self.ghost_mode:
                    return self.trigger_game_over("被Boss子弹击中！")
            if player_head in self.boss.get_body_cells():
                if self.ghost_mode and not self.boss.is_shield_active:
                    self.boss = None
                    self.score += 100
                elif not self.ghost_mode:
                    return self.trigger_game_over("撞到了Boss！")

        foods_pos = [f.pos for f in [self.food, self.energy_food] if f]
        for ai in self.ai_snakes[:]:
            ai.update_ai(foods_pos)
            ai.step()
            ai_head = ai.head()
            if self.food and ai_head == self.food.pos: self.food = None; ai.step(grow=True)
            if self.energy_food and ai_head == self.energy_food.pos: self.energy_food = None; ai.step(grow=True)
            if player_head in ai.body: return self.trigger_game_over("被AI蛇撞到了！")
            if ai_head in self.snake.body:
                self.ai_snakes.remove(ai)
                for _ in range(5):
                    pos = self.random_empty_cell()
                    if pos: self.energy_food = EnergyFood(pos)

        for hunter in self.ghost_hunters:
            if hunter.visible and hunter.get_grid_pos() == player_head and not self.ghost_mode:
                return self.trigger_game_over("被幽灵猎手抓住了！")

        if self.food and player_head == self.food.pos:
            ate_food = True
            self.handle_food_eat(now)
            self.particles.emit(player_head[0] * CELL_SIZE + CELL_SIZE // 2, GAME_AREA_Y + player_head[1] * CELL_SIZE + CELL_SIZE // 2, FOOD_COLOR, 25)
            self.snake.trigger_glow(FOOD_COLOR, now)
            self.food = None
            if self.normal_food_eaten_total % FOOD_PER_OBSTACLE == 0: self.spawn_obstacle()

        if self.energy_food and player_head == self.energy_food.pos:
            ate_food = True # Does not count for combo/boss
            self.energy += 1
            self.particles.emit(player_head[0] * CELL_SIZE + CELL_SIZE // 2, GAME_AREA_Y + player_head[1] * CELL_SIZE + CELL_SIZE // 2, ENERGY_FOOD_COLOR, 30)
            self.snake.trigger_glow(ENERGY_FOOD_COLOR, now)
            self.energy_food = None

        for item in self.items[:]:
            if player_head == item.pos:
                item.apply(self)
                self.items.remove(item)

        if ate_food:
            # Grow by duplicating the last segment (compensates the tail pop in step)
            if self.snake.body:
                self.snake.body.append(self.snake.body[-1])
        # No extra pop here; movement already handled tail removal in step()
        if self.food is None:
            self.spawn_food()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG_COLOR)
        self.draw_grid(surface)
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
        if self.paused: self.draw_leaderboard_overlay(surface)

    def draw_hud(self, surface: pygame.Surface):
        hud_surface = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
        hud_surface.fill((10, 5, 20, 200))
        surface.blit(hud_surface, (0, 0))
        time_left_str = f"{max(0, (self.ghost_end_time - pygame.time.get_ticks()) // 1000)}秒" if self.ghost_mode else "关闭"
        text = f"分数: {self.score}   能量: {self.energy}   幽灵模式: {time_left_str}"
        if self.combo_multiplier > 1:
            text += f"   连击: x{self.combo_multiplier}"
        self.ui.draw_text_with_glow(surface, text, self.ui.font_small, TEXT_COLOR, (8, (HUD_HEIGHT - 18) // 2))
        if self.leaderboard: self.ui.draw_text_with_glow(surface, f"最高分: {self.leaderboard[0]['score']}", self.ui.font_small, (255, 215, 0), (SCREEN_WIDTH - 120, (HUD_HEIGHT - 18) // 2))

    def draw_grid(self, surface: pygame.Surface):
        game_area_end_y = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (x, GAME_AREA_Y), (x, game_area_end_y), 1)
        for y in range(GAME_AREA_Y, game_area_end_y, CELL_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)

    def draw_bottom_bar(self, surface: pygame.Surface):
        if self.energy > 0 and (pygame.time.get_ticks() // 400) % 2:
            bar_y = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT
            bar_surface = pygame.Surface((SCREEN_WIDTH, BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)
            bar_surface.fill((10, 5, 20, 180))
            surface.blit(bar_surface, (0, bar_y))
            self.ui.draw_text_with_glow(surface, "按空格使用幽灵模式技能", self.ui.font_small, (255, 255, 0), (SCREEN_WIDTH // 2, bar_y + BOTTOM_BAR_HEIGHT // 2), center=True)

    def draw_leaderboard_overlay(self, surface: pygame.Surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 5, 20, 230))
        surface.blit(overlay, (0, 0))
        center_x = SCREEN_WIDTH // 2
        self.ui.draw_text_with_glow(surface, "排行榜 TOP 10", self.ui.font_big, (255, 215, 0), (center_x, 40), center=True)
        self.ui.draw_text_with_glow(surface, "(游戏已暂停)", self.ui.font_small, (180, 180, 210), (center_x, 75), center=True)
        y_offset = 110
        if not self.leaderboard: self.ui.draw_text_with_glow(surface, "暂无记录", self.ui.font_small, TEXT_COLOR, (center_x, y_offset + 40), center=True)
        else:
            for i, entry in enumerate(self.leaderboard):
                rank_text, score_text = f"{i+1}. {entry['name']}", f"{entry['score']}"
                color = (255, 215, 0) if i == 0 else (200, 200, 255) if i == 1 else (255, 0, 255) if i == 2 else TEXT_COLOR
                self.ui.draw_text_with_glow(surface, rank_text, self.ui.font_small, color, (center_x - 150, y_offset))
                self.ui.draw_text_with_glow(surface, score_text, self.ui.font_small, color, (center_x + 100, y_offset))
                y_offset += 30
        self.ui.draw_text_with_glow(surface, "按 Tab 返回", self.ui.font_small, (200, 200, 220), (center_x, SCREEN_HEIGHT - 40), center=True)
