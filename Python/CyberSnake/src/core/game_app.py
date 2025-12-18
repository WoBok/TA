import pygame
from typing import Optional, Type, Any

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, RENDER_FPS, EVT_FOOD_EATEN, EVT_ENERGY_EATEN
from .scene import Scene
from .scene_registry import SceneRegistry
from src.managers.ui_manager import UIManager
from src.managers.event_bus import EventBus
from src.managers.resource_loader import ResourceLoader
from src.managers.settings import SettingsService
from src.scenes.scene_catalog import register_default_scenes

class GameApp:
    """Game application, manages window, clock and scene stack.
    Adds a lightweight services container and lifecycle hooks support.
    Also provides a fixed-step update scaffold alongside variable-step rendering.
    """

    def __init__(self, initial_scene_cls: Type[Scene]):
        pygame.init()
        pygame.display.set_caption("CyberSnake")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Try set window icon via resource loader
        try:
            icon_path = ResourceLoader().path("CyberSnake/snake_icon.png")
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        except Exception:
            pass
        self.clock = pygame.time.Clock()
        self.running = True

        # Services container (extendable)
        scenes = SceneRegistry()
        register_default_scenes(scenes)
        self.services: dict[str, Any] = {
            "ui": UIManager(),
            "events": EventBus(),
            "resources": ResourceLoader(),
            "settings": SettingsService(),
            "scenes": scenes,
        }

        self.scene_stack: list[Scene] = []

        # Register default event subscribers
        self._register_default_event_subscribers()

        self.push_scene(initial_scene_cls)

    def push_scene(self, scene_cls: Type[Scene]):
        # Pause current scene
        if self.current_scene:
            try:
                self.current_scene.on_pause()
            except Exception:
                pass
        # Instantiate and enter new scene
        scene = scene_cls(self)
        self.scene_stack.append(scene)
        try:
            scene.on_enter()
        except Exception:
            pass

    def push_scene_key(self, scene_key: str) -> None:
        scenes: SceneRegistry = self.services["scenes"]
        self.push_scene(scenes.get(scene_key))

    def pop_scene(self):
        if self.scene_stack:
            scene = self.scene_stack.pop()
            try:
                scene.on_exit()
            except Exception:
                pass
        if not self.scene_stack:
            self.running = False
        else:
            try:
                self.current_scene.on_resume()
            except Exception:
                pass

    @property
    def current_scene(self) -> Optional[Scene]:
        return self.scene_stack[-1] if self.scene_stack else None

    def _register_default_event_subscribers(self) -> None:
        bus: EventBus = self.services["events"]
        settings = self.services["settings"]
        # Simple console log subscribers depending on settings.log_events
        def on_food_eaten(payload: dict):
            if settings.log_events:
                pos = payload.get("pos")
                score = payload.get("score")
                combo = payload.get("combo")
                print(f"[EVT] FOOD_EATEN pos={pos} score={score} combo={combo}")
        def on_energy_eaten(payload: dict):
            if settings.log_events:
                pos = payload.get("pos")
                energy = payload.get("energy")
                print(f"[EVT] ENERGY_EATEN pos={pos} energy={energy}")
        bus.subscribe(EVT_FOOD_EATEN, on_food_eaten)
        bus.subscribe(EVT_ENERGY_EATEN, on_energy_eaten)

    def run(self):
        fixed_dt = 1.0 / 60.0
        accumulator = 0.0
        while self.running:
            frame_dt = self.clock.tick(RENDER_FPS) / 1000.0
            accumulator += frame_dt

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            scene = self.current_scene
            if not scene:
                break

            # Events first (may push/pop scenes)
            scene.handle_events(events)

            # Fixed-step updates (deterministic logic)
            # Re-fetch scene in case stack changed in handle_events
            scene = self.current_scene
            while self.running and scene and accumulator >= fixed_dt:
                scene.update_fixed(fixed_dt)
                accumulator -= fixed_dt
                scene = self.current_scene

            # Variable-step update (animations/transitions)
            if self.running and self.current_scene:
                self.current_scene.update(frame_dt)

            # Render
            self.screen.fill(BG_COLOR)
            if self.current_scene:
                self.current_scene.draw(self.screen)
            # Optional FPS display
            if self.services.get("settings") and self.services["settings"].show_fps:
                fps = self.clock.get_fps()
                # Render FPS as small corner text using UIManager
                try:
                    ui = self.services["ui"]
                    fps_text = f"FPS: {fps:.0f}"
                    ui.draw_text_with_glow(self.screen, fps_text, ui.font_small, (180, 220, 255), (8, SCREEN_HEIGHT - 22))
                except Exception:
                    pass
            pygame.display.flip()

        pygame.quit()

