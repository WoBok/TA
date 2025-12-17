import pygame
from dataclasses import dataclass
from typing import Tuple

@dataclass
class InputState:
    move_dir: Tuple[int, int] | None = None
    toggle_ghost: bool = False
    paused_toggle: bool = False
    quit: bool = False

class InputManager:
    def __init__(self):
        self.inverted: bool = False  # for rotten apple effect

    def set_inverted(self, inverted: bool):
        self.inverted = inverted

    def poll(self) -> InputState:
        state = InputState()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                state.quit = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    state.quit = True
                elif e.key in (pygame.K_SPACE,):
                    state.toggle_ghost = True
                elif e.key == pygame.K_TAB:
                    state.paused_toggle = True
                elif e.key in (pygame.K_UP, pygame.K_w):
                    state.move_dir = (0, -1)
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    state.move_dir = (0, 1)
                elif e.key in (pygame.K_LEFT, pygame.K_a):
                    state.move_dir = (-1, 0)
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    state.move_dir = (1, 0)
        if self.inverted and state.move_dir:
            dx, dy = state.move_dir
            state.move_dir = (-dx, -dy)
        return state

