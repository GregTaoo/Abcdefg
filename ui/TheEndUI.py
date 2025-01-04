import pygame

import Config
from ui.UI import UI


class TheEndUI(UI):

    def __init__(self):
        super().__init__()
        with open('./assets/lang/end.txt', 'r') as f:
            self.text = f.read().split('\n')
            self.text_surface = pygame.Surface((Config.SCREEN_WIDTH, 1200 + len(self.text) * 50))
            for i, line in enumerate(self.text):
                text_surface = Config.FONT.render(line, True, (255, 255, 255))
                self.text_surface.blit(text_surface, (400 - text_surface.get_width() // 2, 800 + i * 50))
        self.ticks = 0

    def tick(self, keys, events):
        super().tick(keys, events)
        self.ticks += 1
        return self.ticks <= self.text_surface.get_height()

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self.text_surface, (0, -self.ticks))
