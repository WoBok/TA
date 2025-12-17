import pygame
from config import TEXT_COLOR

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

