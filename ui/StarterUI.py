import math
import random

import pygame

import Config
import I18n
from ui.SelectLanguageUI import SelectLanguageUI
from ui.UI import UI


class StarterUI(UI):

    def __init__(self):
        super().__init__()
        self.splash = 'NULL'
        with open('./assets/lang/splashes.txt', 'r') as f:
            self.splash = random.choice(f.readlines())
        self.rendered_splash = pygame.transform.rotate(Config.MIDDLE_FONT.render(self.splash, True, (255, 255, 0)), -30)
        self.tick_cnt = 0

    def tick(self, keys, events):
        super().tick(keys, events)
        self.tick_cnt = (self.tick_cnt + 1) % 90
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                Config.CLIENT.open_ui(SelectLanguageUI())
        return True

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        text_surface = Config.FONT.render(I18n.literal('Click to start.' + '.' * (self.tick_cnt // 30)).get(),
                                          True, (255, 255, 255))
        screen.blit(text_surface,
                    ((Config.SCREEN_WIDTH - text_surface.get_width()) // 2, Config.SCREEN_HEIGHT // 2 + 150))
        scale_factor = 0.75 + 0.25 * math.sin(self.tick_cnt / 45 * math.pi)
        scaled_splash = pygame.transform.scale(self.rendered_splash,
                                               (int(self.rendered_splash.get_width() * scale_factor),
                                                int(self.rendered_splash.get_height() * scale_factor)))
        screen.blit(scaled_splash, (400 - scaled_splash.get_width() // 2, 400 - scaled_splash.get_height() // 2))
