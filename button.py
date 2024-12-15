import pygame


class Button:
    def __init__(self, text, pos, size, font, bg_color=(255, 255, 255), text_color=(0, 0, 0), on_click=lambda: None,
                 border_color=(0, 0, 0), hover_bg_color=(0, 0, 0), hover_text_color=(255, 255, 255),
                 inactive_bg_color=(100, 100, 100), inactive_text_color=(50, 50, 50)):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.hover_bg_color = hover_bg_color
        self.hover_text_color = hover_text_color
        self.inactive_bg_color = inactive_bg_color
        self.inactive_text_color = inactive_text_color
        self.rect = pygame.Rect(pos, size)
        self.on_click = on_click
        self.active = True
        self.hovered = False

    def render(self, screen):
        if not self.active:
            bg_color = self.inactive_bg_color
            text_color = self.inactive_text_color
        elif self.hovered:
            bg_color = self.hover_bg_color
            text_color = self.hover_text_color
        else:
            bg_color = self.bg_color
            text_color = self.text_color
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, width=1)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def tick(self, events):
        if not self.active:
            return
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.on_click()

    def set_active(self, active):
        self.active = active
