import pygame
from typing import Optional, Type

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, RENDER_FPS
from .scene import Scene

class GameApp:
    """Game application, manages window, clock and scene stack."""

    def __init__(self, initial_scene_cls: Type[Scene]):
        pygame.init()
        pygame.display.set_caption("CyberSnake")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_stack: list[Scene] = []
        self.push_scene(initial_scene_cls)

    def push_scene(self, scene_cls: Type[Scene]):
        self.scene_stack.append(scene_cls(self))

    def pop_scene(self):
        if self.scene_stack:
            self.scene_stack.pop()
        if not self.scene_stack:
            self.running = False

    @property
    def current_scene(self) -> Optional[Scene]:
        return self.scene_stack[-1] if self.scene_stack else None

    def run(self):
        while self.running:
            dt = self.clock.tick(RENDER_FPS) / 1000.0
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            scene = self.current_scene
            if not scene:
                break

            scene.handle_events(events)
            scene.update(dt)

            self.screen.fill(BG_COLOR)
            scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

