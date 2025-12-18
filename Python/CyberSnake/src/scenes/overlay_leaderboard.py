import pygame
from src.core.scene import Scene
from src.managers.ui_manager import UIManager
from src.managers.leaderboard import load_leaderboard

class LeaderboardOverlayScene(Scene):
    """Modal overlay that shows TOP 10 leaderboard.
    Close with Tab or ESC to return to previous scene.
    """
    def __init__(self, app):
        super().__init__(app)
        self.ui: UIManager = self.app.services["ui"]
        self.leaderboard = load_leaderboard()
        self.subtitle: str | None = None

    def with_subtitle(self, text: str):
        self.subtitle = text
        return self

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
            if e.type == pygame.KEYDOWN and (e.key == pygame.K_TAB or e.key == pygame.K_ESCAPE):
                self.app.pop_scene()

    def update_fixed(self, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        # Draw underlying scene (if any) first
        if len(self.app.scene_stack) >= 2:
            try:
                self.app.scene_stack[-2].draw(surface)
            except Exception:
                self._maybe_print_exception()
        self.ui.draw_leaderboard_overlay(surface, self.leaderboard, subtitle=self.subtitle)
