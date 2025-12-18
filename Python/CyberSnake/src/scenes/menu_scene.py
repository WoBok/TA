import pygame

from src.core.scene import Scene
from src.managers.leaderboard import load_leaderboard
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, TEXT_COLOR, GRID_COLOR, CELL_SIZE

class MenuScene(Scene):
    """Start menu, shows title, high score, and instructions.
    Handles navigation to GameScene or showing the leaderboard.
    """
    def __init__(self, app):
        super().__init__(app)
        self.ui = self.app.services["ui"]
        self.leaderboard = load_leaderboard()
        self.grid_surface = None
        self._build_grid_surface()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.app.running = False
                elif e.key == pygame.K_SPACE:
                    from src.scenes.game_scene import GameScene
                    self.app.push_scene(GameScene)
                elif e.key == pygame.K_TAB:
                    from src.scenes.overlay_leaderboard import LeaderboardOverlayScene
                    self.app.push_scene(LeaderboardOverlayScene)
                elif e.key == pygame.K_o:
                    from src.scenes.overlay_settings import SettingsOverlayScene
                    self.app.push_scene(SettingsOverlayScene)

    def update(self, dt: float) -> None:
        pass

    def _build_grid_surface(self):
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(surf, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(surf, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        self.grid_surface = surf

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG_COLOR)
        if self.grid_surface:
            surface.blit(self.grid_surface, (0, 0))
        self.draw_start_screen(surface)

    def draw_start_screen(self, surface: pygame.Surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        pulse = abs((pygame.time.get_ticks() % 2000) / 1000 - 1)
        title_color = (int(255), int(100 + pulse * 100), int(200 + pulse * 55))
        self.ui.draw_text_with_glow(surface, "技能贪吃蛇", self.ui.font_xlarge, title_color, (center_x, center_y - 60), center=True)
        self.ui.draw_text_with_glow(surface, "幽灵模式 + 动态障碍", self.ui.font_small, TEXT_COLOR, (center_x, center_y - 10), center=True)

        if self.leaderboard:
            high_score_text = f"最高分: {self.leaderboard[0]['score']} ({self.leaderboard[0]['name']})"
            self.ui.draw_text_with_glow(surface, high_score_text, self.ui.font_medium, (255, 215, 0), (center_x, center_y + 80), center=True)
        else:
            self.ui.draw_text_with_glow(surface, "暂无记录", self.ui.font_medium, (150, 150, 150), (center_x, center_y + 40), center=True)

        blink = (pygame.time.get_ticks() // 800) % 2
        tip_color = (220 if blink else 150, 220 if blink else 150, 255)
        self.ui.draw_text_with_glow(surface, "按空格键开始 (ESC 退出)", self.ui.font_small, tip_color, (center_x, SCREEN_HEIGHT - 60), center=True)
        self.ui.draw_text_with_glow(surface, "方向键/WASD 移动 | 空格: 幽灵模式 | Tab: 排行榜", self.ui.font_small, (190, 190, 210), (center_x, SCREEN_HEIGHT - 35), center=True)

