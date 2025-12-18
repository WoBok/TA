import pygame

from src.core.scene import Scene
from src.managers.ui_manager import UIManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class HelpOverlayScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.ui: UIManager = self.app.services["ui"]

    def _maybe_print_exception(self) -> None:
        try:
            settings = self.app.services.get("settings")
            if settings and getattr(settings, "debug_exceptions", False):
                import traceback

                traceback.print_exc()
        except Exception:
            pass

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN and (e.key in (pygame.K_h, pygame.K_TAB, pygame.K_ESCAPE)):
                self.app.pop_scene()

    def update_fixed(self, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if len(self.app.scene_stack) >= 2:
            try:
                self.app.scene_stack[-2].draw(surface)
            except Exception:
                self._maybe_print_exception()

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 5, 20, 220))
        surface.blit(overlay, (0, 0))

        cx = SCREEN_WIDTH // 2
        y = 60
        self.ui.draw_text_with_glow(surface, "帮助", self.ui.font_big, (0, 255, 255), (cx, y), center=True)
        y += 60

        lines = [
            "方向键/WASD: 移动",
            "空格: 幽灵模式",
            "Tab: 排行榜",
            "P: 暂停",
            "O: 设置",
            "H: 帮助",
            "ESC: 返回/退出",
        ]
        for line in lines:
            self.ui.draw_text_with_glow(surface, line, self.ui.font_small, (200, 220, 255), (cx, y), center=True)
            y += 32

        self.ui.draw_text_with_glow(surface, "按 H/Tab/ESC 返回", self.ui.font_small, (200, 200, 220), (cx, SCREEN_HEIGHT - 40), center=True)
