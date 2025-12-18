import pygame
from src.core.scene import Scene
from src.managers.ui_manager import UIManager

class SettingsOverlayScene(Scene):
    """Modal overlay to toggle runtime settings.
    Keys:
      F - toggle show_fps
      L - toggle log_events
      Tab/ESC - close
    """
    def __init__(self, app):
        super().__init__(app)
        self.ui: UIManager = self.app.services["ui"]
        self.settings = self.app.services["settings"]

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB or e.key == pygame.K_ESCAPE:
                    self.app.pop_scene()
                elif e.key == pygame.K_f:
                    self.settings.show_fps = not self.settings.show_fps
                elif e.key == pygame.K_l:
                    self.settings.log_events = not self.settings.log_events

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
        # overlay
        w, h = surface.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((10, 5, 20, 220))
        surface.blit(overlay, (0, 0))

        cx, cy = w // 2, h // 2
        self.ui.draw_text_with_glow(surface, "设置", self.ui.font_big, (0, 255, 255), (cx, cy - 120), center=True)

        fps_state = "开" if self.settings.show_fps else "关"
        log_state = "开" if self.settings.log_events else "关"
        self.ui.draw_text_with_glow(surface, f"F - 显示 FPS: {fps_state}", self.ui.font_small, (200, 220, 255), (cx, cy - 40), center=True)
        self.ui.draw_text_with_glow(surface, f"L - 事件日志: {log_state}", self.ui.font_small, (200, 220, 255), (cx, cy), center=True)

        self.ui.draw_text_with_glow(surface, "Tab/ESC 返回", self.ui.font_small, (200, 200, 220), (cx, h - 40), center=True)

