import pygame

import config
import i18n
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Hud:

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface):
        pass


class MainHud(Hud):

    def __init__(self, player):
        self.player = player
        config.COIN_IMAGE = pygame.transform.scale(pygame.image.load('assets/coin.png'), (20, 20))

    def tick(self, keys, events):
        pass

    def render(self, screen: pygame.Surface):
        txt_surface = config.FONT.render(i18n.text('player_pos').format(
            i18n.text(config.CLIENT.dimension.name), self.player.x, self.player.y), True, (200, 200, 200))
        screen.blit(txt_surface, (10, 10))
        txt_surface = config.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(config.COIN_IMAGE, (SCREEN_WIDTH - 10 - txt_surface.get_width() - 25, 8))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), 10))
        txt_surface = config.FONT.render(i18n.text('player_values').format(
            self.player.atk, self.player.crt * 100, (self.player.crt_damage - 1) * 100), True, (255, 255, 255))
        screen.blit(txt_surface, (SCREEN_WIDTH - 10 - txt_surface.get_width(), SCREEN_HEIGHT - 30))
