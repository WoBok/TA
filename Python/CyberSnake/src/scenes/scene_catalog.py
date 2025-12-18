from __future__ import annotations

from src.core.scene_registry import SceneRegistry
from src.scenes.scene_keys import (
    SCENE_GAME,
    SCENE_GAME_OVER,
    SCENE_MENU,
    SCENE_OVERLAY_LEADERBOARD,
    SCENE_OVERLAY_HELP,
    SCENE_OVERLAY_PAUSE,
    SCENE_OVERLAY_SETTINGS,
)


def register_default_scenes(registry: SceneRegistry) -> None:
    from src.scenes.menu_scene import MenuScene
    from src.scenes.game_scene import GameScene
    from src.scenes.game_over_scene import GameOverScene
    from src.scenes.overlay_leaderboard import LeaderboardOverlayScene
    from src.scenes.overlay_help import HelpOverlayScene
    from src.scenes.overlay_pause import PauseOverlayScene
    from src.scenes.overlay_settings import SettingsOverlayScene

    registry.register(SCENE_MENU, MenuScene)
    registry.register(SCENE_GAME, GameScene)
    registry.register(SCENE_GAME_OVER, GameOverScene)
    registry.register(SCENE_OVERLAY_LEADERBOARD, LeaderboardOverlayScene)
    registry.register(SCENE_OVERLAY_HELP, HelpOverlayScene)
    registry.register(SCENE_OVERLAY_PAUSE, PauseOverlayScene)
    registry.register(SCENE_OVERLAY_SETTINGS, SettingsOverlayScene)
