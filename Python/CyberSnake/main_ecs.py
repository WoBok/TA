"""
CyberSnake - ECS版本主入口
使用新的ECS架构和插件系统
"""

from src.core.game_app import GameApp
from src.scenes.ecs_game_scene import ECSGameScene

if __name__ == "__main__":
    app = GameApp(initial_scene_cls=ECSGameScene)
    app.run()
