from __future__ import annotations

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BOTTOM_BAR_HEIGHT, HUD_HEIGHT, TEXT_COLOR


class HudRenderer:
    def draw_hud(self, game, surface: pygame.Surface) -> None:
        hud_surface = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
        hud_surface.fill((10, 5, 20, 200))
        surface.blit(hud_surface, (0, 0))

        time_left_str = (
            f"{max(0, (game.ghost_end_time - pygame.time.get_ticks()) // 1000)}秒" if game.ghost_mode else "关闭"
        )
        text = f"分数: {game.score}   能量: {game.energy}   幽灵模式: {time_left_str}"
        if game.combo_multiplier > 1:
            text += f"   连击: x{game.combo_multiplier}"

        text_surf = game.ui.font_small.render(text, True, TEXT_COLOR)
        text_h = text_surf.get_height()
        text_y = max(4, (HUD_HEIGHT - text_h) // 2)
        if HUD_HEIGHT - (text_y + text_h) < 4:
            text_y = HUD_HEIGHT - text_h - 4

        game.ui.draw_text_with_glow(surface, text, game.ui.font_small, TEXT_COLOR, (8, text_y))

        if game.leaderboard:
            hs_text = f"最高分: {game.leaderboard[0]['score']}"
            hs_surf = game.ui.font_small.render(hs_text, True, (255, 215, 0))
            hs_h = hs_surf.get_height()
            hs_y = max(4, (HUD_HEIGHT - hs_h) // 2)
            if HUD_HEIGHT - (hs_y + hs_h) < 4:
                hs_y = HUD_HEIGHT - hs_h - 4
            game.ui.draw_text_with_glow(
                surface,
                hs_text,
                game.ui.font_small,
                (255, 215, 0),
                (SCREEN_WIDTH - 120, hs_y),
            )

    def draw_bottom_bar(self, game, surface: pygame.Surface) -> None:
        if game.energy > 0 and (pygame.time.get_ticks() // 400) % 2:
            bar_y = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT
            bar_surface = pygame.Surface((SCREEN_WIDTH, BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)
            bar_surface.fill((10, 5, 20, 180))
            surface.blit(bar_surface, (0, bar_y))
            game.ui.draw_text_with_glow(
                surface,
                "按空格使用幽灵模式技能",
                game.ui.font_small,
                (255, 255, 0),
                (SCREEN_WIDTH // 2, bar_y + BOTTOM_BAR_HEIGHT // 2),
                center=True,
            )
