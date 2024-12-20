import pygame

import Config
from UI.widget.Button import Button


class ClassicButton(Button):
    def __init__(self, text, pos, size, bg_color=(255, 255, 255), text_color=(0, 0, 0), on_click=lambda: None,
                 border_color=(0, 0, 0), hover_bg_color=(200, 200, 200), hover_text_color=(0, 0, 0),
                 inactive_bg_color=(100, 100, 100), inactive_text_color=(50, 50, 50)):
        super().__init__(pos, size, on_click)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.hover_bg_color = hover_bg_color
        self.hover_text_color = hover_text_color
        self.inactive_bg_color = inactive_bg_color
        self.inactive_text_color = inactive_text_color

    def render(self, screen):
        if not self.active:
            bg_color = self.inactive_bg_color
            text_color = self.inactive_text_color
        elif self.hovered or self.mouse_down:
            bg_color = self.hover_bg_color
            text_color = self.hover_text_color
        else:
            bg_color = self.bg_color
            text_color = self.text_color
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, self.border_color, self.rect, width=1, border_radius=8)
        self.render_text(screen, text_color)

    def render_text(self, screen, text_color):
        text_surface = Config.FONT.render(self.text.get(), True, text_color)
        center = (self.rect.center[0] + 1, self.rect.center[1] + 1) if self.mouse_down else self.rect.center
        text_rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, text_rect)
