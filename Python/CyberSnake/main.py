from src.core.game_app import GameApp
from src.scenes.menu_scene import MenuScene

if __name__ == "__main__":
    # Launch the game with the restored ECS architecture and all original features
    # Starting from MenuScene for full menu/game/game-over flow
    app = GameApp(initial_scene_cls=MenuScene)
    app.run()
