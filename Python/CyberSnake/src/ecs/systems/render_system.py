from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from src.ecs.system import System
from src.ecs.components import (
    PositionComponent,
    RenderComponent,
    BodyComponent,
    SnakeComponent
)
from config import CELL_SIZE, GAME_AREA_Y

if TYPE_CHECKING:
    from src.ecs.world import World

class RenderSystem(System):
    def __init__(self, world: "World", surface: pygame.Surface):
        super().__init__(world)
        self.surface = surface
        self.priority = 100
    
    def update(self, dt: float):
        pass
    
    def render(self):
        entities = self.get_entities_with_components(RenderComponent)
        entities_sorted = sorted(entities, key=lambda e: e.get_component(RenderComponent).layer)
        
        for entity in entities_sorted:
            render_comp = entity.get_component(RenderComponent)
            
            if not render_comp or not render_comp.visible:
                continue
            
            if entity.has_component(BodyComponent):
                self._render_body(entity)
            elif entity.has_component(PositionComponent):
                self._render_simple(entity)
    
    def _render_simple(self, entity):
        pos_comp = entity.get_component(PositionComponent)
        render_comp = entity.get_component(RenderComponent)
        
        if not pos_comp or not render_comp:
            return
        
        cx = pos_comp.x * CELL_SIZE + CELL_SIZE // 2
        cy = GAME_AREA_Y + pos_comp.y * CELL_SIZE + CELL_SIZE // 2
        
        if render_comp.glow_color:
            for r in range(render_comp.radius + 6, render_comp.radius, -1):
                alpha = int(40 * (1 - (r - render_comp.radius) / 6))
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*render_comp.glow_color, alpha), (r, r), r)
                self.surface.blit(s, (cx - r, cy - r))
        
        if render_comp.shape == "circle":
            pygame.draw.circle(self.surface, (*render_comp.color, render_comp.alpha), (cx, cy), render_comp.radius)
        elif render_comp.shape == "square":
            rect = pygame.Rect(cx - render_comp.radius, cy - render_comp.radius, render_comp.radius * 2, render_comp.radius * 2)
            pygame.draw.rect(self.surface, (*render_comp.color, render_comp.alpha), rect)
    
    def _render_body(self, entity):
        body_comp = entity.get_component(BodyComponent)
        render_comp = entity.get_component(RenderComponent)
        snake_comp = entity.get_component(SnakeComponent)
        
        if not body_comp or not render_comp:
            return
        
        for i, (x, y) in enumerate(body_comp.segments):
            cx = x * CELL_SIZE + CELL_SIZE // 2
            cy = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2
            
            is_head = (i == 0)
            radius = render_comp.radius if is_head else int(render_comp.radius * 0.8)
            
            if render_comp.glow_color:
                glow_intensity = 6 if is_head else 4
                for r in range(radius + glow_intensity, radius, -1):
                    alpha = int(30 * (1 - (r - radius) / glow_intensity))
                    s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*render_comp.glow_color, alpha), (r, r), r)
                    self.surface.blit(s, (cx - r, cy - r))
            
            pygame.draw.circle(self.surface, (*render_comp.color, render_comp.alpha), (cx, cy), radius)
