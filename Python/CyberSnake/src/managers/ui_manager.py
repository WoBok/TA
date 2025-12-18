import pygame
from config import TEXT_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT

FONT_CANDIDATES = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "consolas"]

class UIManager:
    def __init__(self):
        self.font_small = pygame.font.SysFont(FONT_CANDIDATES, 18)
        self.font_medium = pygame.font.SysFont(FONT_CANDIDATES, 24, bold=True)
        self.font_big = pygame.font.SysFont(FONT_CANDIDATES, 36, bold=True)
        self.font_xlarge = pygame.font.SysFont(FONT_CANDIDATES, 48, bold=True)

    def draw_text_with_glow(self, surface: pygame.Surface, text: str, font: pygame.font.Font,
                             color: tuple[int, int, int], pos: tuple[int, int], center: bool=False) -> pygame.Rect:
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        if center:
            text_rect.center = pos
        else:
            text_rect.topleft = pos

        glow_color = tuple(max(0, c - 50) for c in color)
        for offset in [(2,2), (-2,2), (2,-2), (-2,-2), (0,2), (0,-2), (2,0), (-2,0)]:
            glow_surf = font.render(text, True, glow_color)
            glow_pos = (text_rect.x + offset[0], text_rect.y + offset[1])
            surface.blit(glow_surf, glow_pos)

        surface.blit(text_surf, text_rect)
        return text_rect

    def draw_leaderboard_overlay(self, surface: pygame.Surface, leaderboard: list,
                                 subtitle: str | None = None,
                                 back_tip: str = "按 Tab 返回") -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 5, 20, 230))
        surface.blit(overlay, (0, 0))

        center_x = SCREEN_WIDTH // 2
        self.draw_text_with_glow(surface, "排行榜 TOP 10", self.font_big, (255, 215, 0), (center_x, 40), center=True)
        y_start = 90
        if subtitle:
            self.draw_text_with_glow(surface, subtitle, self.font_small, (180, 180, 210), (center_x, 75), center=True)
            y_start = 110

        if not leaderboard:
            self.draw_text_with_glow(surface, "暂无记录", self.font_small, TEXT_COLOR, (center_x, y_start + 40), center=True)
        else:
            y_offset = y_start
            current_time = pygame.time.get_ticks()
            for i, entry in enumerate(leaderboard):
                rank_text = f"{i+1}. {entry['name']}"
                score_text = f"{entry['score']}"
                if i == 0:
                    # 第一名：金色闪烁 + 轻微发光描边
                    blink = (current_time // 300) % 2
                    color = (255, 215, 0) if blink else (200, 180, 0)
                    for glow_offset in [(1,1), (-1,1), (1,-1), (-1,-1)]:
                        glow_surf = self.font_small.render(rank_text, True, (255, 200, 50))
                        surface.blit(glow_surf, (center_x - 150 + glow_offset[0], y_offset + glow_offset[1]))
                        glow_surf2 = self.font_small.render(score_text, True, (255, 200, 50))
                        surface.blit(glow_surf2, (center_x + 100 + glow_offset[0], y_offset + glow_offset[1]))
                elif i == 1:
                    # 第二名：紫色脉冲 + 额外发光层
                    pulse = abs((current_time % 1500) / 750 - 1)
                    color = (int(200 + pulse * 55), int(100 + pulse * 100), 255)
                    for glow_offset in range(3, 0, -1):
                        glow_alpha = int(40 * pulse / glow_offset)
                        glow_color = tuple(min(255, c + 50) for c in color)
                        glow_surf = self.font_small.render(rank_text, True, glow_color)
                        glow_surf.set_alpha(glow_alpha)
                        surface.blit(glow_surf, (center_x - 150 - glow_offset, y_offset - glow_offset))
                        glow_surf2 = self.font_small.render(score_text, True, glow_color)
                        glow_surf2.set_alpha(glow_alpha)
                        surface.blit(glow_surf2, (center_x + 100 - glow_offset, y_offset - glow_offset))
                elif i == 2:
                    color = (255, 0, 255)
                else:
                    color = TEXT_COLOR
                self.draw_text_with_glow(surface, rank_text, self.font_small, color, (center_x - 150, y_offset))
                self.draw_text_with_glow(surface, score_text, self.font_small, color, (center_x + 100, y_offset))
                y_offset += 30

        self.draw_text_with_glow(surface, back_tip, self.font_small, (200, 200, 220), (center_x, SCREEN_HEIGHT - 40), center=True)

