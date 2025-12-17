from src.core.game_app import GameApp
from src.scenes.menu_scene import MenuScene

if __name__ == "__main__":
    # Launch the game with the new architecture, starting from the MenuScene.
    app = GameApp(initial_scene_cls=MenuScene)
    app.run()
