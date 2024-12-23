import pygame

import Config
import I18n
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton
from Config import SCREEN_WIDTH, SCREEN_HEIGHT


class DeathUI(UI):

    def __init__(self):
        super().__init__()
        self.add_button(ClassicButton(I18n.text('respawn'), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50),
                                      (200, 50), on_click=lambda: Config.CLIENT.player_respawn()))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.LARGE_FONT.render(I18n.text('you_died').get(), True, (255, 255, 255))
        screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2 + 1, SCREEN_HEIGHT // 2 - 74))
        txt_surface = Config.LARGE_FONT.render(I18n.text('you_died').get(), True, (255, 0, 0))
        screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 75))
