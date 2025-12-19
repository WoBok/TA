import pygame
import random
import time
from pathlib import Path
from typing import List, Optional

from src.core.scene import Scene
from src.ecs.world import World
from src.ecs.event_bus import EventBus
from src.ecs.components import (
    PositionComponent,
    VelocityComponent,
    BodyComponent,
    RenderComponent,
    SnakeComponent,
    FoodComponent,
    SpawnComponent,
    ObstacleComponent,
    EnemyComponent,
    PortalComponent,
    TrapComponent
)
from src.ecs.systems import (
    MovementSystem,
    CollisionSystem,
    RenderSystem,
    SpawnSystem,
    AISystem,
    EffectSystem
)
from src.plugins.plugin_manager import PluginManager
from src.systems.hud_renderer import HudRenderer
from src.managers.input_manager import InputManager
from src.managers.leaderboard import load_leaderboard, save_leaderboard
from src.entities.particle import ParticleSystem
from src.scenes.scene_keys import (
    SCENE_GAME_OVER,
    SCENE_MENU,
    SCENE_OVERLAY_LEADERBOARD,
    SCENE_OVERLAY_PAUSE,
    SCENE_OVERLAY_SETTINGS,
    SCENE_OVERLAY_HELP,
)

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GAME_AREA_Y, BG_COLOR, GRID_COLOR, 
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, BOTTOM_BAR_HEIGHT,
    SNAKE_COLOR, SNAKE_HEAD_COLOR, SNAKE_GLOW, GHOST_DURATION,
    STEP_INTERVAL_MS, FOOD_PER_OBSTACLE
)

class ECSGameScene(Scene):
    def __init__(self, app: "GameApp"):
        super().__init__(app)
        
        self.ui = self.app.services["ui"]
        self.settings = self.app.services["settings"]
        
        self.world = World()
        self.event_bus = EventBus()
        
        self.plugin_manager = PluginManager(self.world, self.event_bus)
        
        plugins_dir = Path(__file__).parent.parent.parent / "plugins"
        self.plugin_manager.add_plugin_directory(plugins_dir)
        self.plugin_manager.discover_plugins()
        
        self.movement_system = MovementSystem(self.world, GRID_WIDTH, GRID_HEIGHT)
        self.collision_system = CollisionSystem(self.world, self.event_bus)
        self.render_system = RenderSystem(self.world, None)
        self.spawn_system = SpawnSystem(self.world, self.plugin_manager, GRID_WIDTH, GRID_HEIGHT)
        self.ai_system = AISystem(self.world, self.plugin_manager)
        self.effect_system = EffectSystem(self.world)
        
        self.world.add_system(self.spawn_system)
        self.world.add_system(self.movement_system)
        self.world.add_system(self.ai_system)
        self.world.add_system(self.collision_system)
        self.world.add_system(self.effect_system)
        
        self.hud_renderer = HudRenderer()
        self.input_manager = InputManager()
        self.particles = ParticleSystem()
        self.leaderboard = load_leaderboard()
        
        self.score = 0
        self.energy = 1
        self.normal_food_eaten_total = 0
        self.food_for_boss_counter = 0
        self.combo_multiplier = 1
        self.last_food_eat_time = 0
        self.combo_window = 2000
        
        self.ghost_mode = False
        self.ghost_end_time = 0
        
        self.magnet_active = False
        self.magnet_end_time = 0
        self.magnet_radius = 5
        
        self.inverted_until = 0
        self.rainbow_trail_until = 0
        
        self.game_over = False
        self.game_over_reason = ""
        
        self.step_accumulator = 0.0
        self.step_interval = STEP_INTERVAL_MS / 1000.0
        
        self.last_obstacle_spawn = 0
        self.last_item_spawn = 0
        self.last_ai_spawn = 0
        
        self.grid_surface = None
        self._build_grid_surface()
        
        self._subscribe_to_events()
        self._initialize_game()
    
    def _subscribe_to_events(self):
        self.event_bus.subscribe("food_eaten", self._on_food_eaten)
        self.event_bus.subscribe("game_over", self._on_game_over)
        self.event_bus.subscribe("apply_snake_modifier", self._on_apply_snake_modifier)
        self.event_bus.subscribe("obstacle_collision", self._on_obstacle_collision)
        self.event_bus.subscribe("enemy_collision", self._on_enemy_collision)
        self.event_bus.subscribe("snake_self_collision", self._on_snake_self_collision)
        self.event_bus.subscribe("snake_grew", self._on_snake_grew)
        self.event_bus.subscribe("energy_gained", self._on_energy_gained)
        self.event_bus.subscribe("snake_shrunk", self._on_snake_shrunk)
        self.event_bus.subscribe("magnet_activated", self._on_magnet_activated)
        self.event_bus.subscribe("bomb_exploded", self._on_bomb_exploded)
        self.event_bus.subscribe("score_boost_collected", self._on_score_boost)
        self.event_bus.subscribe("inverted_controls_activated", self._on_inverted_controls)
        self.event_bus.subscribe("ghost_mode_activated", self._on_ghost_mode_activated)
        self.event_bus.subscribe("food_eaten_original", self._on_food_eaten_original)
        self.event_bus.subscribe("boss_defeated", self._on_boss_defeated)
    
    def _initialize_game(self):
        self.player_entity = self._create_player_snake()
        
        spawn_entity = self.world.create_entity()
        spawn_comp = SpawnComponent()
        spawn_comp.spawn_type = "food"
        spawn_comp.spawn_interval = 0.0
        spawn_comp.max_spawns = 1
        spawn_entity.add_component(spawn_comp)
        
        self._spawn_initial_food()
    
    def _create_player_snake(self):
        entity = self.world.create_entity()
        
        start_x, start_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        body_comp = BodyComponent()
        body_comp.segments = [(start_x, start_y), (start_x - 1, start_y)]
        entity.add_component(body_comp)
        
        vel_comp = VelocityComponent()
        vel_comp.direction = (1, 0)
        entity.add_component(vel_comp)
        
        snake_comp = SnakeComponent()
        snake_comp.is_player = True
        snake_comp.next_direction = (1, 0)
        entity.add_component(snake_comp)
        
        render_comp = RenderComponent()
        render_comp.color = SNAKE_COLOR
        render_comp.glow_color = SNAKE_GLOW
        render_comp.radius = 10
        render_comp.layer = 3
        entity.add_component(render_comp)
        
        entity.add_tag("player")
        entity.add_tag("snake")
        
        return entity
    
    def _spawn_initial_food(self):
        position = self._find_empty_position()
        if position:
            food_plugins = self.plugin_manager.get_all_food_plugins()
            if food_plugins:
                food_plugin = random.choice(food_plugins)
                food_plugin.create_food(self.world, position)
    
    def _find_empty_position(self):
        from src.ecs.components import PositionComponent, BodyComponent
        
        occupied = set()
        
        for entity in self.world.get_all_entities():
            if entity.has_component(PositionComponent):
                pos_comp = entity.get_component(PositionComponent)
                if pos_comp:
                    occupied.add(pos_comp.pos)
            
            if entity.has_component(BodyComponent):
                body_comp = entity.get_component(BodyComponent)
                if body_comp:
                    occupied.update(body_comp.segments)
        
        possible_positions = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if (x, y) not in occupied:
                    possible_positions.append((x, y))
        
        return random.choice(possible_positions) if possible_positions else None
    
    def _on_food_eaten(self, payload):
        snake_entity = payload.get("snake_entity")
        food_entity = payload.get("food_entity")
        
        if not food_entity or not snake_entity:
            return
        
        food_comp = food_entity.get_component(FoodComponent)
        if food_comp:
            self.score += food_comp.score_value
            
            food_type = food_comp.food_type
            food_plugin = self.plugin_manager.get_food_plugin(food_type)
            if food_plugin:
                food_plugin.on_food_eaten(self.world, self.event_bus, food_entity, snake_entity)
        
        self._spawn_initial_food()
    
    def _on_apply_snake_modifier(self, payload):
        modifier_type = payload.get("modifier_type")
        snake_entity = payload.get("snake_entity")
        
        if not modifier_type or not snake_entity:
            return
        
        modifier_plugin = self.plugin_manager.get_snake_modifier_plugin(modifier_type)
        if modifier_plugin:
            modifier_plugin.apply_modifier(self.world, self.event_bus, snake_entity, payload)
    
    def _on_obstacle_collision(self, payload):
        if payload.get("deadly", True):
            self.game_over = True
            self.game_over_reason = "Hit obstacle"
    
    def _on_enemy_collision(self, payload):
        self.game_over = True
        self.game_over_reason = "Hit enemy"
    
    def _on_snake_self_collision(self, payload):
        snake_entity = payload.get("snake_entity")
        if snake_entity:
            snake_comp = snake_entity.get_component(SnakeComponent)
            if snake_comp and not snake_comp.ghost_mode:
                self.game_over = True
                self.game_over_reason = "Hit yourself"
    
    def _on_game_over(self, payload):
        self.game_over = True
        self.game_over_reason = payload.get("reason", "Game Over")
    
    def _on_snake_grew(self, payload):
        pass
    
    def _on_energy_gained(self, payload):
        amount = payload.get("amount", 1)
        self.energy += amount
    
    def _on_snake_shrunk(self, payload):
        removed_parts = payload.get("removed_parts", [])
        for pos in removed_parts:
            px = pos[0] * CELL_SIZE + CELL_SIZE // 2
            py = GAME_AREA_Y + pos[1] * CELL_SIZE + CELL_SIZE // 2
            self.particles.emit(px, py, (100, 200, 255), count=15)
    
    def _on_magnet_activated(self, payload):
        self.magnet_active = True
        self.magnet_radius = payload.get("radius_cells", 5)
        duration_ms = payload.get("duration_ms", 5000)
        self.magnet_end_time = pygame.time.get_ticks() + duration_ms
    
    def _on_bomb_exploded(self, payload):
        position = payload.get("position")
        if position:
            px = position[0] * CELL_SIZE + CELL_SIZE // 2
            py = GAME_AREA_Y + position[1] * CELL_SIZE + CELL_SIZE // 2
            self.particles.emit(px, py, (255, 100, 0), count=50)
    
    def _on_score_boost(self, payload):
        bonus = payload.get("bonus", 25)
        self.score += bonus
    
    def _on_inverted_controls(self, payload):
        duration_ms = payload.get("duration_ms", 5000)
        now = pygame.time.get_ticks()
        self.inverted_until = now + duration_ms
        self.rainbow_trail_until = now + duration_ms
        self.input_manager.set_inverted(True)
    
    def _on_ghost_mode_activated(self, payload):
        self.ghost_mode = True
        duration_ms = payload.get("duration_ms", GHOST_DURATION)
        self.ghost_end_time = pygame.time.get_ticks() + duration_ms
    
    def _on_food_eaten_original(self, payload):
        now = pygame.time.get_ticks()
        
        if now - self.last_food_eat_time < self.combo_window:
            self.combo_multiplier = min(8, self.combo_multiplier * 2)
        else:
            self.combo_multiplier = 1
        
        self.last_food_eat_time = now
        self.score += self.combo_multiplier
        self.normal_food_eaten_total += 1
        self.food_for_boss_counter += 1
        
        if self.food_for_boss_counter >= 10:
            self.food_for_boss_counter = 0
            self._spawn_boss()
        
        if self.normal_food_eaten_total % FOOD_PER_OBSTACLE == 0:
            self._spawn_obstacle()
    
    def _on_boss_defeated(self, payload):
        self.score += 100
        px = GRID_WIDTH // 2 * CELL_SIZE + CELL_SIZE // 2
        py = GAME_AREA_Y + GRID_HEIGHT // 2 * CELL_SIZE + CELL_SIZE // 2
        self.particles.emit(px, py, (255, 200, 0), count=100)
    
    def _spawn_obstacle(self):
        position = self._find_empty_position()
        if position:
            obstacle_plugins = [p for p in self.plugin_manager.get_all_obstacle_plugins() if p.get_obstacle_type() == "original_static"]
            if obstacle_plugins:
                obstacle_plugins[0].create_obstacle(self.world, position)
    
    def _spawn_boss(self):
        position = self._find_empty_position()
        if position:
            boss_plugins = [p for p in self.plugin_manager.get_all_enemy_plugins() if p.is_boss()]
            if boss_plugins:
                boss_plugins[0].create_enemy(self.world, position)
    
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        if self.game_over:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.app.push_scene_key(SCENE_MENU)
                    elif e.key == pygame.K_RETURN:
                        self.world.clear()
                        self._initialize_game()
                        self.game_over = False
                        self.score = 0
                        self.energy = 1
                        self.normal_food_eaten_total = 0
                        self.food_for_boss_counter = 0
                        self.combo_multiplier = 1
            return
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                direction = None
                if e.key in (pygame.K_UP, pygame.K_w): direction = (0, -1)
                elif e.key in (pygame.K_DOWN, pygame.K_s): direction = (0, 1)
                elif e.key in (pygame.K_LEFT, pygame.K_a): direction = (-1, 0)
                elif e.key in (pygame.K_RIGHT, pygame.K_d): direction = (1, 0)
                
                if direction and self.player_entity:
                    if self.input_manager.inverted:
                        direction = (-direction[0], -direction[1])
                    
                    snake_comp = self.player_entity.get_component(SnakeComponent)
                    vel_comp = self.player_entity.get_component(VelocityComponent)
                    if snake_comp and vel_comp:
                        current_dir = vel_comp.direction
                        if (current_dir[0] + direction[0], current_dir[1] + direction[1]) != (0, 0):
                            snake_comp.next_direction = direction
                
                elif e.key == pygame.K_SPACE:
                    if self.energy > 0 and not self.ghost_mode:
                        self.energy -= 1
                        self.event_bus.publish("apply_snake_modifier", {
                            "modifier_type": "ghost_mode",
                            "snake_entity": self.player_entity,
                            "duration_ms": GHOST_DURATION
                        })
                
                elif e.key == pygame.K_TAB:
                    self.app.push_scene_key(SCENE_OVERLAY_LEADERBOARD)
                    overlay = self.app.current_scene
                    try:
                        overlay.with_subtitle("(游戏已暂停)")
                    except Exception:
                        pass
                
                elif e.key == pygame.K_p:
                    self.app.push_scene_key(SCENE_OVERLAY_PAUSE)
                
                elif e.key == pygame.K_o:
                    self.app.push_scene_key(SCENE_OVERLAY_SETTINGS)
                
                elif e.key == pygame.K_h:
                    self.app.push_scene_key(SCENE_OVERLAY_HELP)
                
                elif e.key == pygame.K_ESCAPE:
                    self.app.push_scene_key(SCENE_MENU)
    
    def update_fixed(self, dt: float) -> None:
        if self.game_over:
            return
        
        self.step_accumulator += dt
        
        while self.step_accumulator >= self.step_interval:
            body_comp = self.player_entity.get_component(BodyComponent)
            if body_comp and len(body_comp.segments) > 2:
                body_comp.segments.pop()
            
            self.world.update(self.step_interval)
            self.event_bus.process_events()
            
            self.step_accumulator -= self.step_interval
    
    def update(self, dt: float) -> None:
        if self.game_over:
            return
        
        now = pygame.time.get_ticks()
        
        # Update particles
        self.particles.update()
        
        # Update magnet effect
        if self.magnet_active and now >= self.magnet_end_time:
            self.magnet_active = False
        
        if self.magnet_active and self.player_entity:
            body_comp = self.player_entity.get_component(BodyComponent)
            if body_comp:
                head_pos = body_comp.head()
                # Pull food towards player
                for food_entity in self.world.get_entities_with_tag("food"):
                    pos_comp = food_entity.get_component(PositionComponent)
                    if pos_comp:
                        fx, fy = pos_comp.pos
                        hx, hy = head_pos
                        if (hx - fx)**2 + (hy - fy)**2 <= self.magnet_radius ** 2:
                            new_fx = fx + (1 if hx > fx else -1 if hx < fx else 0)
                            new_fy = fy + (1 if hy > fy else -1 if hy < fy else 0)
                            pos_comp.x = new_fx
                            pos_comp.y = new_fy
                            self.particles.emit(
                                new_fx * CELL_SIZE + CELL_SIZE // 2,
                                GAME_AREA_Y + new_fy * CELL_SIZE + CELL_SIZE // 2,
                                (255, 255, 100), count=2
                            )
        
        # Update inverted controls
        if self.input_manager.inverted and now >= self.inverted_until:
            self.input_manager.set_inverted(False)
        
        if now >= self.rainbow_trail_until:
            self.rainbow_trail_until = 0
        
        # Update ghost mode
        if self.ghost_mode and now >= self.ghost_end_time:
            self.ghost_mode = False
            if self.player_entity:
                snake_comp = self.player_entity.get_component(SnakeComponent)
                if snake_comp:
                    snake_comp.ghost_mode = False
        
        # Update combo multiplier
        if now - self.last_food_eat_time > self.combo_window:
            self.combo_multiplier = 1
        
        # Update obstacle plugins (for traps, lava pools, etc.)
        for entity in self.world.get_entities_with_components(ObstacleComponent):
            obstacle_comp = entity.get_component(ObstacleComponent)
            if obstacle_comp:
                obstacle_plugin = self.plugin_manager.get_obstacle_plugin(obstacle_comp.obstacle_type)
                if obstacle_plugin:
                    obstacle_plugin.update_obstacle(self.world, entity, dt)
    
    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG_COLOR)
        
        if self.grid_surface:
            surface.blit(self.grid_surface, (0, 0))
        
        # Draw all entities except snake
        self.render_system.surface = surface
        for entity in self.world.get_all_entities():
            if not entity.has_tag("player"):
                render_comp = entity.get_component(RenderComponent)
                if render_comp and render_comp.visible:
                    if entity.has_component(BodyComponent):
                        self._draw_body_entity(surface, entity)
                    elif entity.has_component(PositionComponent):
                        self._draw_simple_entity(surface, entity)
        
        # Draw player snake with special effects
        if self.player_entity:
            self._draw_player_snake(surface)
        
        # Draw particles
        self.particles.draw(surface)
        
        # Draw HUD
        self._draw_hud(surface)
        self._draw_bottom_bar(surface)
        
        if self.game_over:
            self._draw_game_over(surface)
    
    def _draw_simple_entity(self, surface: pygame.Surface, entity):
        pos_comp = entity.get_component(PositionComponent)
        render_comp = entity.get_component(RenderComponent)
        
        if not pos_comp or not render_comp:
            return
        
        cx = int(pos_comp.x * CELL_SIZE + CELL_SIZE // 2)
        cy = int(GAME_AREA_Y + pos_comp.y * CELL_SIZE + CELL_SIZE // 2)
        
        if render_comp.glow_color:
            for r in range(render_comp.radius + 6, render_comp.radius, -1):
                alpha = int(40 * (1 - (r - render_comp.radius) / 6))
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*render_comp.glow_color, alpha), (r, r), r)
                surface.blit(s, (cx - r, cy - r))
        
        if render_comp.shape == "circle":
            pygame.draw.circle(surface, (*render_comp.color, render_comp.alpha), (cx, cy), render_comp.radius)
        elif render_comp.shape == "square":
            rect = pygame.Rect(cx - render_comp.radius, cy - render_comp.radius, render_comp.radius * 2, render_comp.radius * 2)
            s = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.rect(s, (*render_comp.color, render_comp.alpha), s.get_rect())
            surface.blit(s, rect)
    
    def _draw_body_entity(self, surface: pygame.Surface, entity):
        body_comp = entity.get_component(BodyComponent)
        render_comp = entity.get_component(RenderComponent)
        
        if not body_comp or not render_comp:
            return
        
        for i, (x, y) in enumerate(body_comp.segments):
            cx = int(x * CELL_SIZE + CELL_SIZE // 2)
            cy = int(GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2)
            
            is_head = (i == 0)
            radius = render_comp.radius if is_head else int(render_comp.radius * 0.8)
            
            if render_comp.glow_color:
                glow_intensity = 6 if is_head else 4
                for r in range(radius + glow_intensity, radius, -1):
                    alpha = int(30 * (1 - (r - radius) / glow_intensity))
                    s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*render_comp.glow_color, alpha), (r, r), r)
                    surface.blit(s, (cx - r, cy - r))
            
            pygame.draw.circle(surface, (*render_comp.color, render_comp.alpha), (cx, cy), radius)
    
    def _draw_player_snake(self, surface: pygame.Surface):
        body_comp = self.player_entity.get_component(BodyComponent)
        snake_comp = self.player_entity.get_component(SnakeComponent)
        render_comp = self.player_entity.get_component(RenderComponent)
        vel_comp = self.player_entity.get_component(VelocityComponent)
        
        if not body_comp or not render_comp:
            return
        
        # Calculate ghost alpha
        ghost_alpha = None
        if self.ghost_mode:
            time_left = max(0, self.ghost_end_time - pygame.time.get_ticks())
            interval = 50 if time_left < 2000 else 100 if time_left < 3000 else 150
            ghost_alpha = 120 if (pygame.time.get_ticks() // interval) % 2 == 0 else 200
        
        # Check rainbow trail
        rainbow_effect = pygame.time.get_ticks() < self.rainbow_trail_until
        
        snake_len = len(body_comp.segments)
        now_alpha = 255 if ghost_alpha is None else ghost_alpha
        
        # Glow effect progress
        glow_progress = -1.0
        if snake_comp and snake_comp.glow_effect_active and snake_comp.glow_effect_color:
            elapsed = pygame.time.get_ticks() - snake_comp.glow_effect_start
            if elapsed < snake_comp.glow_effect_duration:
                glow_progress = elapsed / snake_comp.glow_effect_duration
            else:
                snake_comp.glow_effect_active = False
        
        for i, (x, y) in enumerate(body_comp.segments):
            cx = int(x * CELL_SIZE + CELL_SIZE // 2)
            cy = int(GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2)
            
            is_head = (i == 0)
            radius = CELL_SIZE // 2 - 1 if is_head else int(CELL_SIZE * 0.42)
            base_color = SNAKE_HEAD_COLOR if is_head else SNAKE_COLOR
            glow_color = SNAKE_HEAD_COLOR if is_head else SNAKE_GLOW
            
            # Gradient to tail
            if snake_len > 1:
                factor = i / max(1, snake_len - 1)
                base_color = tuple(int(base_color[c] * (1 - factor * 0.3)) for c in range(3))
            
            # Glow effect color mixing
            is_glowing = False
            if glow_progress >= 0 and snake_len > 0 and snake_comp and snake_comp.glow_effect_color:
                glow_pos = glow_progress * snake_len
                glow_width = 3
                if abs(i - glow_pos) < glow_width:
                    is_glowing = True
                    dist_factor = 1.0 - abs(i - glow_pos) / glow_width
                    blend = dist_factor * 0.9
                    base_color = tuple(
                        min(255, int((base_color[c] * (1 - blend) + snake_comp.glow_effect_color[c] * blend) * 1.3))
                        for c in range(3)
                    )
                    glow_color = tuple(min(255, int(snake_comp.glow_effect_color[c] * 1.2)) for c in range(3))
            
            # Rainbow effect
            if rainbow_effect and not is_head:
                hue = (pygame.time.get_ticks() + i * 35) % 360
                c = pygame.Color(0)
                c.hsla = (hue, 100, 50, now_alpha)
                base_color = (c.r, c.g, c.b)
                glow_color = base_color
            
            # Draw glow
            glow_intensity = 6 if is_glowing else 4
            for r in range(radius + glow_intensity, radius, -1):
                alpha_glow = int((30 if is_glowing else 20) * (1 - (r - radius) / glow_intensity))
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*glow_color, alpha_glow), (r, r), r)
                surface.blit(s, (cx - r, cy - r))
            
            # Draw body
            ball = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ball, (*base_color, now_alpha), (radius, radius), radius)
            
            # Highlight
            highlight_radius = int(radius * 0.6)
            hx_off = int(radius * 0.3)
            hy_off = int(radius * 0.3)
            highlight_color = tuple(min(255, c + 80) for c in base_color)
            hl_alpha = int(now_alpha * 0.8) if now_alpha < 255 else 200
            pygame.draw.circle(ball, (*highlight_color, hl_alpha), (radius - hx_off, radius - hy_off), highlight_radius)
            
            # Small highlight
            small_r = int(radius * 0.3)
            sx_off = int(radius * 0.4)
            sy_off = int(radius * 0.4)
            pygame.draw.circle(ball, (255, 255, 255, min(now_alpha, 180)), (radius - sx_off, radius - sy_off), small_r)
            
            surface.blit(ball, (cx - radius, cy - radius))
            
            # Draw eyes on head
            if is_head and vel_comp:
                dx, dy = vel_comp.direction
                eye_size = max(2, radius // 4)
                forward = radius // 2
                side = radius // 3
                if dx == 1:
                    e1 = (cx + forward, cy - side)
                    e2 = (cx + forward, cy + side)
                elif dx == -1:
                    e1 = (cx - forward, cy - side)
                    e2 = (cx - forward, cy + side)
                elif dy == -1:
                    e1 = (cx - side, cy - forward)
                    e2 = (cx + side, cy - forward)
                else:
                    e1 = (cx - side, cy + forward)
                    e2 = (cx + side, cy + forward)
                
                # Eye glow
                for rr in range(eye_size + 2, eye_size, -1):
                    a = int(60 * (1 - (rr - eye_size) / 2))
                    s = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (255, 255, 255, a), (rr, rr), rr)
                    surface.blit(s, (e1[0] - rr, e1[1] - rr))
                    surface.blit(s, (e2[0] - rr, e2[1] - rr))
                
                # Eye white
                pygame.draw.circle(surface, (255, 255, 255), e1, eye_size)
                pygame.draw.circle(surface, (255, 255, 255), e2, eye_size)
                
                # Pupil
                pupil = max(1, eye_size // 2)
                pygame.draw.circle(surface, (0, 0, 0), e1, pupil)
                pygame.draw.circle(surface, (0, 0, 0), e2, pupil)
    
    def _draw_hud(self, surface: pygame.Surface):
        # Use HUD renderer for consistent styling
        self.hud_renderer.draw_hud(self, surface)
    
    def _draw_bottom_bar(self, surface: pygame.Surface):
        # Use HUD renderer for bottom bar
        self.hud_renderer.draw_bottom_bar(self, surface)
    
    def _draw_game_over(self, surface: pygame.Surface):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        font_tiny = pygame.font.Font(None, 24)
        
        # Game over text with glow
        game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
        glow_text = font_large.render("GAME OVER", True, (255, 100, 100))
        
        x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2
        y = SCREEN_HEIGHT // 2 - 100
        
        for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            surface.blit(glow_text, (x + offset[0], y + offset[1]))
        surface.blit(game_over_text, (x, y))
        
        # Reason
        reason_text = font_small.render(self.game_over_reason, True, (255, 255, 255))
        surface.blit(reason_text, (SCREEN_WIDTH // 2 - reason_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        
        # Score
        score_text = font_small.render(f"Final Score: {self.score}", True, (0, 255, 255))
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        
        # Stats
        stats_text = font_tiny.render(f"Food Eaten: {self.normal_food_eaten_total}", True, (200, 200, 200))
        surface.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        
        # Instructions
        restart_text = font_small.render("Press ENTER to restart or ESC for menu", True, (200, 200, 200))
        surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        
        # Check if score qualifies for leaderboard
        if self.leaderboard and len(self.leaderboard) < 10 or (self.leaderboard and self.score > min(entry['score'] for entry in self.leaderboard)):
            qualify_text = font_tiny.render("New High Score!", True, (255, 255, 0))
            surface.blit(qualify_text, (SCREEN_WIDTH // 2 - qualify_text.get_width() // 2, SCREEN_HEIGHT // 2 + 140))
    
    def _build_grid_surface(self):
        game_area_end_y = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        border_color = (100, 50, 150)
        pygame.draw.line(surf, border_color, (0, GAME_AREA_Y), (SCREEN_WIDTH, GAME_AREA_Y), 2)
        pygame.draw.line(surf, border_color, (0, GAME_AREA_Y), (0, game_area_end_y), 2)
        pygame.draw.line(surf, border_color, (0, game_area_end_y - 1), (SCREEN_WIDTH, game_area_end_y - 1), 2)
        pygame.draw.line(surf, border_color, (SCREEN_WIDTH - 1, GAME_AREA_Y), (SCREEN_WIDTH - 1, game_area_end_y), 2)
        
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(surf, GRID_COLOR, (x, GAME_AREA_Y), (x, game_area_end_y), 1)
        for y in range(GAME_AREA_Y, game_area_end_y, CELL_SIZE):
            pygame.draw.line(surf, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        
        bright_grid = (80, 40, 120)
        for x in range(0, SCREEN_WIDTH, CELL_SIZE * 5):
            pygame.draw.line(surf, bright_grid, (x, GAME_AREA_Y), (x, game_area_end_y), 2)
        for y in range(GAME_AREA_Y, game_area_end_y, CELL_SIZE * 5):
            pygame.draw.line(surf, bright_grid, (0, y), (SCREEN_WIDTH, y), 2)
        
        self.grid_surface = surf
