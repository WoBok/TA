import pygame
from src.core.scene import Scene
from src.managers.ui_manager import UIManager

class PauseOverlayScene(Scene):
    """Modal pause overlay. Press P/ESC to resume."""
    def __init__(self, app):
        super().__init__(app)
        self.ui: UIManager = self.app.services["ui"]

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN and (e.key == pygame.K_p or e.key == pygame.K_ESCAPE):
                self.app.pop_scene()

    def update_fixed(self, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        # draw underlying scene first
        if len(self.app.scene_stack) >= 2:
            try:
                self.app.scene_stack[-2].draw(surface)
            except Exception:
                pass
        w, h = surface.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((10, 5, 20, 200))
        surface.blit(overlay, (0, 0))
        cx, cy = w // 2, h // 2
        self.ui.draw_text_with_glow(surface, "已暂停", self.ui.font_big, (255, 215, 0), (cx, cy - 20), center=True)
        self.ui.draw_text_with_glow(surface, "按 P 或 ESC 返回", self.ui.font_small, (200, 200, 220), (cx, h - 40), center=True)

