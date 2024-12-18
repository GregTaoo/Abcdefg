import pygame

import UI
import config
import i18n
from button import ImageButton
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Hud:

    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def tick(self, keys, events):
        for button in self.buttons:
            button.tick(events)

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            button.render(screen)


class MainHud(Hud):

    def __init__(self, player):
        super().__init__()
        self.player = player
        config.COIN_IMAGE = pygame.transform.scale(pygame.image.load('assets/coin.png'), (20, 20))
        config.LANGUAGE_IMAGE = pygame.transform.scale(pygame.image.load('assets/language.png'), (20, 20))
        self.add_button(ImageButton(config.LANGUAGE_IMAGE, (10, SCREEN_HEIGHT - 30),
                                    lambda: config.CLIENT.open_ui(UI.SelectLanguageUI())))

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = config.FONT.render(i18n.text('player_pos').format(
            i18n.text(config.CLIENT.dimension.name), self.player.x, self.player.y), True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
        txt_surface = config.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(config.COIN_IMAGE, (SCREEN_WIDTH - 10 - txt_surface.get_width() - 25, 8))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), 10))
        txt_surface = config.FONT.render(i18n.text('player_values').format(
            self.player.atk, self.player.crt * 100, (self.player.crt_damage - 1) * 100), True, (255, 255, 255))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), SCREEN_HEIGHT - 30))
