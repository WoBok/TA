import pygame

from src.core.scene import Scene
from src.managers.leaderboard import is_high_score, add_entry, save_leaderboard
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, TEXT_COLOR
from src.scenes.scene_keys import SCENE_GAME, SCENE_MENU, SCENE_OVERLAY_LEADERBOARD, SCENE_OVERLAY_HELP

class GameOverScene(Scene):
    """Displays final score, handles high score entry, and offers restart/exit options."""

    def __init__(self, app):
        super().__init__(app)
        self.ui = self.app.services["ui"]
        self.score = 0
        self.reason = ""
        self.leaderboard = []
        self.entering_name = False
        self.player_name_input = ""

    def set_stats(self, score: int, reason: str, leaderboard: list):
        """Receives final stats from the game scene."""
        self.score = score
        self.reason = reason
        self.leaderboard = leaderboard
        if self.score > 0 and is_high_score(self.leaderboard, self.score):
            self.entering_name = True
        else:
            self.entering_name = False

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
                self.app.push_scene_key(SCENE_OVERLAY_LEADERBOARD)
                continue
            if e.type == pygame.KEYDOWN and e.key == pygame.K_h:
                self.app.push_scene_key(SCENE_OVERLAY_HELP)
                continue

            if self.entering_name:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        name = self.player_name_input.strip() or "Anonymous"
                        self.leaderboard = add_entry(self.leaderboard, name, self.score)
                        save_leaderboard(self.leaderboard)
                        self.entering_name = False
                    elif e.key == pygame.K_BACKSPACE:
                        self.player_name_input = self.player_name_input[:-1]
                    elif e.key == pygame.K_ESCAPE:
                        self.entering_name = False
                    elif len(self.player_name_input) < 15:
                        self.player_name_input += e.unicode
            else:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        self.app.push_scene_key(SCENE_GAME)
                    elif e.key == pygame.K_ESCAPE:
                        self.app.push_scene_key(SCENE_MENU)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG_COLOR)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 5, 20, 180))
        surface.blit(overlay, (0, 0))

        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        if self.entering_name:
            self.draw_name_input(surface, center_x, center_y)
        else:
            self.draw_game_over_summary(surface, center_x, center_y)

        # 排行榜覆盖层由独立的 LeaderboardOverlayScene 负责

    def draw_name_input(self, surface, cx, cy):
        self.ui.draw_text_with_glow(surface, "新纪录！", self.ui.font_big, (255, 215, 0), (cx, cy - 80), center=True)
        self.ui.draw_text_with_glow(surface, "请输入你的名字：", self.ui.font_small, TEXT_COLOR, (cx, cy - 30), center=True)
        
        input_box = pygame.Rect(cx - 150, cy, 300, 40)
        pygame.draw.rect(surface, (30, 20, 50), input_box, border_radius=3)
        pygame.draw.rect(surface, (0, 255, 255), input_box, 2, border_radius=3)
        
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 else " "
        self.ui.draw_text_with_glow(surface, self.player_name_input + cursor, self.ui.font_small, (255, 255, 255), (input_box.x + 10, input_box.y + 10))
        self.ui.draw_text_with_glow(surface, "回车确认，ESC 跳过", self.ui.font_small, (200, 200, 220), (cx, cy + 60), center=True)

    def draw_game_over_summary(self, surface, cx, cy):
        self.ui.draw_text_with_glow(surface, "游戏结束", self.ui.font_big, (255, 0, 127), (cx, cy - 60), center=True)
        self.ui.draw_text_with_glow(surface, self.reason, self.ui.font_small, TEXT_COLOR, (cx, cy - 10), center=True)
        self.ui.draw_text_with_glow(surface, f"最终得分: {self.score}", self.ui.font_small, (255, 255, 0), (cx, cy + 60), center=True)
        
        if self.leaderboard:
            high_score_text = f"最高分: {self.leaderboard[0]['score']} ({self.leaderboard[0]['name']})"
            self.ui.draw_text_with_glow(surface, high_score_text, self.ui.font_medium, (255, 215, 0), (cx, cy + 90), center=True)
        
        self.ui.draw_text_with_glow(surface, "按 R 重新开始，ESC 返回菜单", self.ui.font_small, (200, 200, 220), (cx, SCREEN_HEIGHT - 40), center=True)


