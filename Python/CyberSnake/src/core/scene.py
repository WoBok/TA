import pygame

class Scene:
    """Base class for all scenes.
    Subclasses should implement event handling, update, and draw.
    """

    def __init__(self, app: "GameApp"):
        self.app = app

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        raise NotImplementedError

    def update(self, dt: float) -> None:
        raise NotImplementedError

    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError

