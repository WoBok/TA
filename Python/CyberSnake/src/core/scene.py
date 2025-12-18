import pygame

class Scene:
    """Base class for all scenes.
    Subclasses should implement event handling, update, and draw.
    Provides lifecycle hooks and a fixed-step update hook for extensibility.
    """

    def __init__(self, app: "GameApp"):
        self.app = app

    # Lifecycle hooks (optional override)
    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def on_pause(self) -> None:
        pass

    def on_resume(self) -> None:
        pass

    # Event handling and updates (must override at least these 3)
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        raise NotImplementedError

    def update_fixed(self, dt: float) -> None:
        """Fixed-step update. Default no-op. Override to run deterministic logic."""
        pass

    def update(self, dt: float) -> None:
        raise NotImplementedError

    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError

