from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, List
import random
import time

from src.plugins.plugin_interface import EnemyPlugin
from src.ecs.components import (
    PositionComponent, RenderComponent, BodyComponent, VelocityComponent,
    EnemyComponent, AIComponent, CollisionComponent, HealthComponent
)
from config import GRID_WIDTH, GRID_HEIGHT

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class AISnakePlugin(EnemyPlugin):
    def get_enemy_type(self) -> str:
        return "ai_snake"
    
    def create_enemy(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        body_comp = BodyComponent()
        body_comp.segments = [position, (position[0]-1, position[1]), (position[0]-2, position[1])]
        entity.add_component(body_comp)
        
        vel_comp = VelocityComponent()
        vel_comp.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        entity.add_component(vel_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (80, 200, 120)
        render_comp.glow_color = (100, 220, 140)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 2
        entity.add_component(render_comp)
        
        enemy_comp = EnemyComponent()
        enemy_comp.enemy_type = "ai_snake"
        enemy_comp.ai_behavior = "chase"
        enemy_comp.damage = 1
        enemy_comp.is_boss = False
        entity.add_component(enemy_comp)
        
        ai_comp = AIComponent()
        ai_comp.behavior = "chase"
        ai_comp.update_interval = 0.1
        entity.add_component(ai_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "enemy"
        entity.add_component(collision_comp)
        
        entity.add_tag("enemy")
        entity.add_tag("ai_snake")
        
        return entity
    
    def update_ai(self, world: "World", enemy_entity: "Entity", dt: float) -> None:
        vel_comp = enemy_entity.get_component(VelocityComponent)
        body_comp = enemy_entity.get_component(BodyComponent)
        
        if not vel_comp or not body_comp:
            return
        
        # Find food entities
        food_entities = world.get_entities_with_tag("food")
        if not food_entities:
            if random.random() < 0.1:
                vel_comp.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            return
        
        # Get positions of all food
        food_positions = []
        for food_entity in food_entities:
            pos_comp = food_entity.get_component(PositionComponent)
            if pos_comp:
                food_positions.append(pos_comp.pos)
        
        if not food_positions:
            return
        
        # Find nearest food
        hx, hy = body_comp.head()
        target = min(food_positions, key=lambda p: abs(p[0]-hx) + abs(p[1]-hy))
        
        dx, dy = target[0] - hx, target[1] - hy
        
        # Prefer horizontal movement
        if dx != 0 and (vel_comp.dx != -dx or vel_comp.dy != 0):
            vel_comp.direction = (1 if dx > 0 else -1, 0)
        elif dy != 0 and (vel_comp.dy != -dy or vel_comp.dx != 0):
            vel_comp.direction = (0, 1 if dy > 0 else -1)
    
    def on_collision(self, world: "World", event_bus: "EventBus", enemy_entity: "Entity", collider_entity: "Entity") -> None:
        event_bus.publish("game_over", {
            "reason": "Hit AI snake",
            "entity": collider_entity
        })
    
    def is_boss(self) -> bool:
        return False
    
    def get_spawn_weight(self) -> float:
        return 5.0

class GhostHunterPlugin(EnemyPlugin):
    def get_enemy_type(self) -> str:
        return "ghost_hunter"
    
    def create_enemy(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        # Use float position for smooth movement
        pos_comp = PositionComponent()
        pos_comp.x = float(position[0])
        pos_comp.y = float(position[1])
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 50, 50)
        render_comp.glow_color = (255, 100, 100)
        render_comp.radius = 12
        render_comp.shape = "circle"
        render_comp.layer = 2
        render_comp.alpha = 150
        entity.add_component(render_comp)
        
        enemy_comp = EnemyComponent()
        enemy_comp.enemy_type = "ghost_hunter"
        enemy_comp.ai_behavior = "hunt"
        enemy_comp.damage = 1
        enemy_comp.is_boss = False
        entity.add_component(enemy_comp)
        
        ai_comp = AIComponent()
        ai_comp.behavior = "hunt"
        ai_comp.update_interval = 0.016
        ai_comp.state = {
            "speed": 0.02,
            "visible": True,
            "next_toggle_time": time.time() + random.uniform(4, 7)
        }
        entity.add_component(ai_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "enemy"
        entity.add_component(collision_comp)
        
        entity.add_tag("enemy")
        entity.add_tag("ghost_hunter")
        
        return entity
    
    def update_ai(self, world: "World", enemy_entity: "Entity", dt: float) -> None:
        pos_comp = enemy_entity.get_component(PositionComponent)
        ai_comp = enemy_entity.get_component(AIComponent)
        render_comp = enemy_entity.get_component(RenderComponent)
        
        if not pos_comp or not ai_comp:
            return
        
        current_time = time.time()
        
        # Toggle visibility
        if current_time > ai_comp.state.get("next_toggle_time", 0):
            ai_comp.state["visible"] = not ai_comp.state.get("visible", True)
            duration = random.uniform(4, 7) if ai_comp.state["visible"] else random.uniform(4, 8)
            ai_comp.state["next_toggle_time"] = current_time + duration
            
            if ai_comp.state["visible"]:
                # Respawn at random edge
                edge = random.choice(['top', 'bottom', 'left', 'right'])
                if edge == 'top':
                    pos_comp.x = random.randint(0, GRID_WIDTH-1)
                    pos_comp.y = -1
                elif edge == 'bottom':
                    pos_comp.x = random.randint(0, GRID_WIDTH-1)
                    pos_comp.y = GRID_HEIGHT
                elif edge == 'left':
                    pos_comp.x = -1
                    pos_comp.y = random.randint(0, GRID_HEIGHT-1)
                else:
                    pos_comp.x = GRID_WIDTH
                    pos_comp.y = random.randint(0, GRID_HEIGHT-1)
        
        if render_comp:
            render_comp.visible = ai_comp.state.get("visible", True)
        
        if not ai_comp.state.get("visible", True):
            return
        
        # Move towards player
        player_entities = world.get_entities_with_tag("player")
        if player_entities:
            player = player_entities[0]
            from src.ecs.components import BodyComponent
            player_body = player.get_component(BodyComponent)
            
            if player_body:
                tx, ty = player_body.head()
                px, py = pos_comp.x, pos_comp.y
                dx, dy = tx - px, ty - py
                dist = (dx**2 + dy**2)**0.5
                
                if dist > 0:
                    speed = ai_comp.state.get("speed", 0.02)
                    pos_comp.x += speed * dx / dist
                    pos_comp.y += speed * dy / dist
    
    def on_collision(self, world: "World", event_bus: "EventBus", enemy_entity: "Entity", collider_entity: "Entity") -> None:
        ai_comp = enemy_entity.get_component(AIComponent)
        if ai_comp and ai_comp.state.get("visible", True):
            event_bus.publish("game_over", {
                "reason": "Caught by ghost hunter",
                "entity": collider_entity
            })
    
    def is_boss(self) -> bool:
        return False
    
    def get_spawn_weight(self) -> float:
        return 0.0

class BossPlugin(EnemyPlugin):
    def get_enemy_type(self) -> str:
        return "boss"
    
    def create_enemy(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        # Boss occupies 3x3 grid
        body_comp = BodyComponent()
        body_cells = []
        for r in range(3):
            for c in range(3):
                body_cells.append((position[0] + c, position[1] + r))
        body_comp.segments = body_cells
        entity.add_component(body_comp)
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (150, 50, 150)
        render_comp.glow_color = (180, 80, 180)
        render_comp.radius = 12
        render_comp.shape = "square"
        render_comp.layer = 3
        entity.add_component(render_comp)
        
        enemy_comp = EnemyComponent()
        enemy_comp.enemy_type = "boss"
        enemy_comp.ai_behavior = "boss"
        enemy_comp.damage = 1
        enemy_comp.is_boss = True
        entity.add_component(enemy_comp)
        
        health_comp = HealthComponent()
        health_comp.current = 1
        health_comp.maximum = 1
        health_comp.invulnerable = True
        entity.add_component(health_comp)
        
        ai_comp = AIComponent()
        ai_comp.behavior = "boss"
        ai_comp.update_interval = 0.016
        ai_comp.state = {
            "shield_end_time": time.time() + 5.0,
            "last_shot_time": 0.0,
            "shot_interval": 1.0,
            "bullets": []
        }
        entity.add_component(ai_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "enemy"
        entity.add_component(collision_comp)
        
        entity.add_tag("enemy")
        entity.add_tag("boss")
        
        return entity
    
    def update_ai(self, world: "World", enemy_entity: "Entity", dt: float) -> None:
        ai_comp = enemy_entity.get_component(AIComponent)
        health_comp = enemy_entity.get_component(HealthComponent)
        pos_comp = enemy_entity.get_component(PositionComponent)
        
        if not ai_comp or not pos_comp:
            return
        
        current_time = time.time()
        
        # Update shield
        if health_comp:
            health_comp.invulnerable = current_time < ai_comp.state.get("shield_end_time", 0)
        
        # Shoot bullets
        if not health_comp or not health_comp.invulnerable:
            if current_time - ai_comp.state.get("last_shot_time", 0) > ai_comp.state.get("shot_interval", 1.0):
                player_entities = world.get_entities_with_tag("player")
                if player_entities:
                    player = player_entities[0]
                    from src.ecs.components import BodyComponent
                    player_body = player.get_component(BodyComponent)
                    
                    if player_body:
                        target_pos = player_body.head()
                        self._shoot_bullet(world, pos_comp.pos, target_pos)
                        ai_comp.state["last_shot_time"] = current_time
        
        # Update bullets
        bullets = ai_comp.state.get("bullets", [])
        for bullet_id in bullets[:]:
            bullet_entity = world.get_entity(bullet_id)
            if bullet_entity:
                bullet_pos = bullet_entity.get_component(PositionComponent)
                bullet_vel = bullet_entity.get_component(VelocityComponent)
                
                if bullet_pos and bullet_vel:
                    bullet_pos.x += bullet_vel.dx
                    bullet_pos.y += bullet_vel.dy
                    
                    # Remove if offscreen
                    if not (0 <= bullet_pos.x < GRID_WIDTH and 0 <= bullet_pos.y < GRID_HEIGHT):
                        bullet_entity.destroy()
                        bullets.remove(bullet_id)
            else:
                bullets.remove(bullet_id)
    
    def _shoot_bullet(self, world: "World", boss_pos: Vec2, target_pos: Vec2):
        start_pos = (boss_pos[0] + 1.5, boss_pos[1] + 1.5)
        dx, dy = target_pos[0] - start_pos[0], target_pos[1] - start_pos[1]
        dist = (dx**2 + dy**2)**0.5
        
        if dist > 0:
            speed = 0.1
            velocity = (dx / dist * speed, dy / dist * speed)
            
            bullet = world.create_entity()
            
            bullet_pos = PositionComponent()
            bullet_pos.x = start_pos[0]
            bullet_pos.y = start_pos[1]
            bullet.add_component(bullet_pos)
            
            bullet_vel = VelocityComponent()
            bullet_vel.dx = velocity[0]
            bullet_vel.dy = velocity[1]
            bullet.add_component(bullet_vel)
            
            bullet_render = RenderComponent()
            bullet_render.color = (255, 100, 100)
            bullet_render.radius = 5
            bullet_render.shape = "circle"
            bullet_render.layer = 2
            bullet.add_component(bullet_render)
            
            bullet_collision = CollisionComponent()
            bullet_collision.collision_layer = "enemy"
            bullet.add_component(bullet_collision)
            
            bullet.add_tag("bullet")
            bullet.add_tag("boss_bullet")
    
    def on_collision(self, world: "World", event_bus: "EventBus", enemy_entity: "Entity", collider_entity: "Entity") -> None:
        health_comp = enemy_entity.get_component(HealthComponent)
        
        if health_comp and not health_comp.invulnerable:
            health_comp.current -= 1
            
            if health_comp.current <= 0:
                event_bus.publish("boss_defeated", {
                    "boss_entity": enemy_entity,
                    "player_entity": collider_entity
                })
                enemy_entity.destroy()
            else:
                event_bus.publish("boss_hit", {
                    "boss_entity": enemy_entity,
                    "player_entity": collider_entity
                })
        else:
            event_bus.publish("game_over", {
                "reason": "Hit boss",
                "entity": collider_entity
            })
    
    def is_boss(self) -> bool:
        return True
    
    def get_spawn_weight(self) -> float:
        return 0.0
