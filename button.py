import pygame


class Button:
    def __init__(self, text, pos, size, font, bg_color, text_color, on_click):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.rect = pygame.Rect(pos, size)
        self.on_click = on_click
        self.active = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def tick(self, events):
        if not self.active:
            return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.on_click()

    def set_active(self, active):
        self.active = active
